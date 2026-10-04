<h1 align="center">🛡️ VulnOps-Scale: Enterprise Patch Velocity Framework for automated vulnerability remediation & software lifecycle governance</h1>


## 📌 Introduction

Ce projet implémente un framework d'automatisation et de gouvernance déterministe conçu pour éliminer la latence opérationnelle entre la détection d'une vulnérabilité et sa remédiation. 

En s'appuyant directement sur l'API de **Tenable Nessus**, ce moteur convertit des rapports de scan en métriques de performance stratégiques (**Patch Velocity**) et oriente les menaces à la vitesse de la machine.

## 🎯 Objectifs du Projet

- 🔄 **Automatisation API :** Interroger Nessus Essentials en direct sans intervention humaine
- 📊 **Calcul de la Patch Velocity :** Mesurer le temps d'arbitrage (en millisecondes) et le volume de traitement
- ⚡ **Taux d'Absorption :** Isoler 100% des vulnérabilités d'OS éligibles à un auto-patching immédiat

## 🏗️ Technical Stack

- **Vulnerability Management :** Tenable Nessus Essentials
- **Orchestrateur & Triage :** Python 3 (Requests, Dotenv)
- **Environnement de Contrôle :** Debian 
- **Environnements évalués :** Linux & Windows



## 🏗️ Architecture du Pipeline VulnOps-Scale

```mermaid
graph TD
    %% Définition du flux principal
    A[🛡️ Nessus Essentials API] -->|Extraction JSON en direct| B(🧠 Moteur Python VulnOps)
    B -->|Horodatage & Calcul de Vélocité| C[📊 Génération Dashboard HTML]
    
    %% Triage déterministe en 3 axes
    B -->|0.2005 secondes| D{⚖️ Sécurisation & Triage Déterministe}
    
    D -->|Filtre OS / Paquets Linux| E[🚀 Axe 1 : Fully Autonomous]
    D -->|Filtre Runtimes & Third-Party Apps| F[🧪 Axe 2 : Test Before Deploy]
    D -->|Filtre IOCs / Malwares / RCE| G[🚨 Axe 3 : Manual Review]

    %% Détails des actions de remédiation
    E -.->|Auto-Patch Velocity| E1[Instantané : Mises à jour Apt/Yum/KB]
    F -.->|Gated Rollout| F1[Validation sur Environnement de Staging]
    G -.->|Incident Response| G1[Alerte SOC immédiate & Levée de doute]

    %% Style visuel du graphique
    style A fill:#2a5298,stroke:#1e3c72,stroke-width:2px,color:#fff
    style B fill:#1e3c72,stroke:#112244,stroke-width:2px,color:#fff
    style C fill:#e67e22,stroke:#d35400,stroke-width:2px,color:#fff
    style D fill:#f1c40f,stroke:#f39c12,stroke-width:2px,color:#222
    style E fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:#fff
    style F fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff
    style G fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff
```

## 🛠️ Installation & Configuration
1. Clonez le dépôt.
2. Créez un fichier `.env` à la racine avec vos clés API Nessus :
   ```env
   NESSUS_ACCESS_KEY=votre_cle
   NESSUS_SECRET_KEY=votre_cle
   NESSUS_URL=https://localhost:8834
   ```
3. Lancez l'orchestrateur : `python3 vulnOps_automator.py

## 🔍 Preuve de Concept & Résultats 

<p align="center">
  <img src="docs/Tenable.login.jpg" width="700">
</p>

### 🔹Scan

![Scan](docs/Start_detection.jpg)

### 🔹Vulnerabilités detectées

![Vulns_detectées](docs/Vulns_detectées.png)

### 🔹 Évaluation de l'Infrastructure  (`Lin-01`)
Lors de l'exécution du pipeline sur notre infrastructure en production, le framework a généré les métriques de vélocité suivantes :

![Scan](docs/reduction_du_MTTR.jpg)



### 🔹RESULTAT 

![Scan](docs/view_vulns.jpg)


## 📖 Documentation

L'intelligence algorithmique et la logique de triage de ce framework s'appuient sur les standards et référentiels de sécurité suivants :

- **[Tenable Nessus API Documentation](https://tenable.com)** 
- **[CISA KEV (Known Exploited Vulnerabilities)](https://cisa.gov)** 
- **[FIRST CVSS v3.1/v4.0 Framework](https://first.org)** 
- **[FIRST EPSS (Exploit Prediction Scoring System)](https://first.org)** 
- **[MITRE ATT&CK Framework](https://mitre.org)** 




<p align="center">
  🛡️ <strong>Hubert Codjo</strong><br>
  <sub>Cybersecurity Engineer • Vulnerability Analyst • </sub><br><br>
  📧 <a href="mailto:houet.hubert@gmail.com"><strong>Click to contact me</strong></a><br><br>
  ─ · ─<br><br>
</p>