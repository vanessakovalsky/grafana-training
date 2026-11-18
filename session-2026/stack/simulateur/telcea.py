#!/usr/bin/env python3
"""Telcea network simulator - Prometheus exporter for the Grafana training.

Fictitious operator: 12 radio sites (4G/5G) in 4 regions, 4 aggregation routers,
3 regional links to the Paris core. Daily traffic cycle (Europe/Paris time).

HTTP (port 9200):
  GET  /metrics        Prometheus metrics
  GET  /etat           current scenario (JSON)
  POST /tempete/start  storm in Brittany (sites down, battery, saturated link)
  POST /tempete/stop   back to normal
Logs (stdout, logfmt): network alarms, collected by Alloy into Loki.
"""
import json
import math
import random
import sys
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from zoneinfo import ZoneInfo

from prometheus_client import (CONTENT_TYPE_LATEST, Counter, Gauge, Histogram,
                               generate_latest)

TZ = ZoneInfo("Europe/Paris")
STEP = 5  # seconds between two simulation steps

# site, city, region, techno, lat, lon, max users
SITES = [
    ("REN-01", "Rennes", "Bretagne", "5G", 48.1173, -1.6778, 900),
    ("BRE-01", "Brest", "Bretagne", "4G", 48.3904, -4.4861, 600),
    ("QUI-01", "Quimper", "Bretagne", "4G", 47.9960, -4.1024, 400),
    ("PAR-01", "Paris La Defense", "Ile-de-France", "5G", 48.8920, 2.2380, 2000),
    ("PAR-02", "Paris Bercy", "Ile-de-France", "5G", 48.8380, 2.3820, 1800),
    ("SDN-01", "Saint-Denis", "Ile-de-France", "4G", 48.9362, 2.3574, 1200),
    ("LIL-01", "Lille", "Hauts-de-France", "5G", 50.6292, 3.0573, 1100),
    ("AMI-01", "Amiens", "Hauts-de-France", "4G", 49.8941, 2.2958, 500),
    ("DUN-01", "Dunkerque", "Hauts-de-France", "4G", 51.0343, 2.3768, 450),
    ("MRS-01", "Marseille", "Provence", "5G", 43.2965, 5.3698, 1500),
    ("TLN-01", "Toulon", "Provence", "4G", 43.1242, 5.9280, 700),
    ("AVI-01", "Avignon", "Provence", "4G", 43.9493, 4.8055, 550),
]
# link, region, capacity (bit/s)
LINKS = [
    ("REN-PAR", "Bretagne", 1e9),
    ("LIL-PAR", "Hauts-de-France", 1e9),
    ("MRS-PAR", "Provence", 1e9),
]
ROUTERS = [("rtr-par-01", "Ile-de-France"), ("rtr-ren-01", "Bretagne"),
           ("rtr-lil-01", "Hauts-de-France"), ("rtr-mrs-01", "Provence")]
STORM_SITES = {"BRE-01", "QUI-01"}       # down during the storm
STORM_BATTERY = {"REN-01"}                # on battery during the storm

S = ["site", "region"]
site_info = Gauge("telcea_site_info", "Static site description (always 1)",
                  ["site", "ville", "region", "techno", "latitude", "longitude"])
site_up = Gauge("telcea_site_up", "Radio site availability (1 up, 0 down)", S + ["techno"])
site_battery = Gauge("telcea_site_on_battery", "Site powered by battery (1 yes, 0 mains)", S)
site_temp = Gauge("telcea_site_temperature_celsius", "Equipment room temperature", S)
cell_users = Gauge("telcea_cell_users", "Subscribers attached to the site", S + ["techno"])
cell_bytes = Counter("telcea_cell_traffic_bytes", "Data traffic of the site",
                     S + ["techno", "direction"])
call_attempts = Counter("telcea_call_attempts", "Voice call attempts", S)
call_failures = Counter("telcea_call_failures", "Failed voice call setups", S)
latency = Histogram("telcea_site_latency_seconds", "Round trip time site to core", S,
                    buckets=(0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.5))
link_capacity = Gauge("telcea_link_capacity_bits_per_second", "Link capacity", ["link", "region"])
link_bytes = Counter("telcea_link_bytes", "Bytes carried by the link", ["link", "region", "direction"])
link_loss = Gauge("telcea_link_packet_loss_ratio", "Packet loss ratio (0-1)", ["link", "region"])
router_cpu = Gauge("telcea_router_cpu_ratio", "Router CPU usage (0-1)", ["router", "region"])

state = {"tempete": False, "depuis": None}
lock = threading.Lock()


def log(level, msg, **labels):
    parts = [f"level={level}"] + [f"{k}={v}" for k, v in labels.items()] + [f'msg="{msg}"']
    print(" ".join(parts), flush=True)


def daily_profile(now):
    """Load factor 0.1 to 1.0: night trough, morning rise, evening peak."""
    h = now.hour + now.minute / 60
    base = 0.1 + 0.6 * max(0.0, math.sin(math.pi * (h - 6) / 18)) if 6 <= h <= 24 else 0.1
    evening = 0.3 * math.exp(-((h - 20.5) ** 2) / 3)
    return min(1.0, base + evening)


def step():
    now = datetime.now(TZ)
    load = daily_profile(now)
    storm = state["tempete"]
    region_bytes = {}
    for site, _ville, region, techno, _lat, _lon, max_users in SITES:
        down = storm and site in STORM_SITES
        battery = storm and site in STORM_BATTERY
        site_up.labels(site, region, techno).set(0 if down else 1)
        site_battery.labels(site, region).set(1 if (down or battery) else 0)
        temp = 22 + 6 * load + random.uniform(-0.5, 0.5) + (9 if battery else 0)
        site_temp.labels(site, region).set(round(temp, 1))
        users = 0 if down else int(max_users * load * random.uniform(0.92, 1.08))
        cell_users.labels(site, region, techno).set(users)
        per_user = 45_000 if techno == "5G" else 18_000  # bytes/s per active user
        down_b = users * per_user * STEP * random.uniform(0.8, 1.2)
        cell_bytes.labels(site, region, techno, "down").inc(down_b)
        cell_bytes.labels(site, region, techno, "up").inc(down_b * 0.12)
        region_bytes[region] = region_bytes.get(region, 0) + down_b * 1.12
        if down:
            continue
        attempts = max(1, int(users * 0.002 * STEP))
        fail_rate = 0.004 + (0.08 if storm and region == "Bretagne" else 0)
        call_attempts.labels(site, region).inc(attempts)
        call_failures.labels(site, region).inc(sum(random.random() < fail_rate for _ in range(attempts)))
        base_rtt = (0.008 if techno == "5G" else 0.025) * (1 + 0.5 * load)
        if storm and region == "Bretagne":
            base_rtt *= 6
        for _ in range(20):
            latency.labels(site, region).observe(random.lognormvariate(math.log(base_rtt), 0.35))
    for link, region, cap in LINKS:
        b = region_bytes.get(region, 0)
        saturated = storm and region == "Bretagne"
        if saturated:  # traffic rerouted from the neighbouring sites
            b = cap / 8 * STEP * random.uniform(0.94, 0.99)
        link_capacity.labels(link, region).set(cap)
        link_bytes.labels(link, region, "out").inc(b * 0.9)
        link_bytes.labels(link, region, "in").inc(b * 0.1)
        loss = random.uniform(0.02, 0.05) if saturated else random.uniform(0, 0.0005)
        link_loss.labels(link, region).set(round(loss, 5))
    for router, region in ROUTERS:
        cpu = 0.15 + 0.45 * load + random.uniform(-0.03, 0.03)
        if storm and region == "Bretagne":
            cpu = random.uniform(0.88, 0.97)
        router_cpu.labels(router, region).set(round(cpu, 3))
    # background noise: a few minor alarms
    if random.random() < 0.02:
        site, _v, region, *_ = random.choice(SITES)
        log("warn", "Seuil de temperature approche", site=site, region=region, code="ENV-101")
    if random.random() < 0.05:
        site, _v, region, *_ = random.choice(SITES)
        log("info", "Supervision OK", site=site, region=region, code="SUP-000")


def set_storm(on):
    with lock:
        if state["tempete"] == on:
            return False
        state["tempete"] = on
        state["depuis"] = datetime.now(TZ).isoformat(timespec="seconds") if on else None
    if on:
        for s in sorted(STORM_SITES):
            log("error", "Perte d'alimentation secteur puis arret du site", site=s,
                region="Bretagne", code="PWR-003")
        for s in sorted(STORM_BATTERY):
            log("warn", "Bascule sur batterie", site=s, region="Bretagne", code="PWR-001")
        log("error", "Saturation du lien de collecte", link="REN-PAR", region="Bretagne", code="TRS-201")
    else:
        for s in sorted(STORM_SITES | STORM_BATTERY):
            log("info", "Retour secteur, site nominal", site=s, region="Bretagne", code="PWR-000")
        log("info", "Lien de collecte nominal", link="REN-PAR", region="Bretagne", code="TRS-200")
    return True


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/metrics":
            self._send(200, generate_latest(), CONTENT_TYPE_LATEST)
        elif self.path in ("/", "/etat"):
            self._send(200, json.dumps(state) + "\n")
        else:
            self._send(404, '{"erreur": "inconnu"}\n')

    def do_POST(self):
        if self.path in ("/tempete/start", "/tempete/stop"):
            changed = set_storm(self.path.endswith("start"))
            self._send(200, json.dumps({**state, "modifie": changed}) + "\n")
        else:
            self._send(404, '{"erreur": "inconnu"}\n')

    def log_message(self, *args):  # keep stdout for network alarms only
        pass


def main():
    for site, ville, region, techno, lat, lon, _ in SITES:
        site_info.labels(site, ville, region, techno, str(lat), str(lon)).set(1)
    log("info", "Demarrage du simulateur Telcea", sites=len(SITES), links=len(LINKS))
    server = ThreadingHTTPServer(("0.0.0.0", 9200), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    while True:
        try:
            with lock:
                step()
        except Exception as exc:  # never stop the exporter
            print(f"level=error msg=\"step failed: {exc}\"", file=sys.stderr, flush=True)
        time.sleep(STEP)


if __name__ == "__main__":
    main()
