FROM python:3.13.18-slim
RUN pip install --no-cache-dir prometheus-client==0.26.0 tzdata
# Pas de series *_created (bruit pour un public debutant)
ENV PROMETHEUS_DISABLE_CREATED_SERIES=True
WORKDIR /app
COPY telcea.py .
USER nobody
EXPOSE 9200
CMD ["python", "-u", "telcea.py"]
