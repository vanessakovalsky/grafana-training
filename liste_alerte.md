# Définition des alertes pertinentes pour notre projet :

A partir du tableau de bord fait pendant les exercices précédents définir : 
* Quelles alertes seraient pertinentes sur nos métriques ?
* Quel seuil ou contrainte faut t'il prendre en compte pour la définitions des règles d'alertes ?
* Qui doit on prévenir ?


## Exemples d'alertes pertinentes

* Alerte Usage CPU par conteneur > 80%. 80% limite du service non rendu. Equipe -> exploitant VM / conteneur. Questionnement : si service perdu à 80%, pertinence de prévenir avant la limite atteinte et le service non rendu.
* ESX, CPU / RAM / Disque . >70% . -> Admin vcenter
* Alimentation : verification des sondes d'alimentation. Si l'alim est down, alerte. -> proximité pour changement d'alimentation.
* Trafic réseau : pic réseau anormal (montée du trafic) : % de la capacité du réseau. -> équipe réseau, sécurité (après vérification côté réseau de la légitimité du trafic)
* Service down : necessite que la métrique (service up/down) existe. -> gestionnaire du service
* Nombre de vm / conteneurs minimum qui doivent fonctionner : seuil défini par l'architecture; -> equipe appli/cluster
* Traffic sortant : pic non prévu fonctionnellement, risque de sécurité (exfiltration de données) -> équipe métier / sécurité 
