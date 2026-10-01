import os
import sys
import time
import json
import requests
import urllib3
from dotenv import load_workbook, load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ACCESS_KEY = os.getenv("NESSUS_ACCESS_KEY")
SECRET_KEY = os.getenv("NESSUS_SECRET_KEY")
NESSUS_URL = os.getenv("NESSUS_URL", "https://localhost:8834")

if not ACCESS_KEY or not SECRET_KEY:
    print("[-] Erreur : NESSUS_ACCESS_KEY et NESSUS_SECRET_KEY doivent être définies dans un fichier .env")
    sys.exit(1)

headers = {
    "X-ApiKeys": f"accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}",
    "Content-Type": "application/json"
}

def select_scan_interactively():
    url = f"{NESSUS_URL}/scans"
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            print(f"[-] Impossible de lister les scans : {response.text}")
            sys.exit(1)
        
        scans_list = response.json().get("scans", [])
        if not scans_list:
            print("[-] Aucun scan trouvé dans Nessus.")
            sys.exit(1)
            
        print("[*] Scans disponibles dans votre Nessus :")
        for idx, scan in enumerate(scans_list):
            print(f"  [{idx}] ID: {scan['id']} | Nom: {scan['name']} | Statut: {scan['status']}")
            
        print("\n[*] Entrez le numéro du scan à analyser : ", end="")
        try:
            choice = int(input())
            if choice < 0 or choice >= len(scans_list):
                raise ValueError
            return scans_list[choice]["id"]
        except (ValueError, IndexError):
            print("[-] Choix invalide. Sélection du premier scan par défaut.")
            return scans_list[0]["id"]
    except Exception as e:
        print(f"[-] Erreur de connexion à Nessus : {e}")
        sys.exit(1)

def get_scan_details(scan_id):
    url = f"{NESSUS_URL}/scans/{scan_id}"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        print(f"[-] Échec de la récupération des détails : {response.text}")
        sys.exit(1)
    return response.json()

def process_vulnops_velocity_framework(scan_data, start_time):
    metrics = {
        "total_critical_high_vulns": 0,
        "autonomous_eligible_vulns": 0,
        "absorption_rate_percent": 0.0,
        "triage_velocity_seconds": 0.0
    }
    report = {"1_fully_autonomous": [], "2_test_before_deploy": [], "3_manual_review": []}

    vulnerabilities = scan_data.get("vulnerabilities", [])
    hosts = scan_data.get("hosts", [])
    
    host_name = "Target-Host"
    if hosts and isinstance(hosts, list) and len(hosts) > 0:
        host_name = hosts[0].get("hostname", "Target-Host")

    for vuln in vulnerabilities:
        severity = vuln.get("severity", 0)
        plugin_name = vuln.get("plugin_name", "")
        plugin_id = vuln.get("plugin_id", "")
        
        is_actionable = severity >= 3

        if is_actionable:
            metrics["total_critical_high_vulns"] += 1

        vuln_details = {"host": host_name, "plugin_id": plugin_id, "name": plugin_name, "severity_score": severity}

        if any(x in plugin_name.lower() for x in ["malware", "virus", "backdoor", "trojan", "ms17-010", "eternalblue"]):
            report["3_manual_review"].append(vuln_details)
        elif is_actionable and any(x in plugin_name.lower() for x in ["windows update", "kb", "missing patch", "debian", "ubuntu", "redhat", "security update", "linux kernel"]):
            report["1_fully_autonomous"].append(vuln_details)
            metrics["autonomous_eligible_vulns"] += 1
        elif is_actionable:
            report["2_test_before_deploy"].append(vuln_details)

    end_time = time.time()
    metrics["triage_velocity_seconds"] = round(end_time - start_time, 4)
    if metrics["total_critical_high_vulns"] > 0:
        metrics["absorption_rate_percent"] = round((metrics["autonomous_eligible_vulns"] / metrics["total_critical_high_vulns"]) * 100, 2)

    return report, metrics

if __name__ == "__main__":
    print("[*] ========================================================")
    print("[*] VulnOps-Scale Enterprise Patch Velocity Framework v1.5")
    print("[*] ========================================================\n")
    
    scan_id = select_scan_interactively()
    start_triage = time.time()
    
    print(f"\n[+] Extraction des données du Scan ID: {scan_id}...")
    scan_data = get_scan_details(scan_id)
    report, metrics = process_vulnops_velocity_framework(scan_data, start_triage)
    
    with open("vulnops_triage_output.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
        
    with open("vulnops_velocity_metrics.json", "w", encoding="utf-8") as mf:
        json.dump(metrics, mf, indent=4)
        
    print("\n[+] --- EXECUTIVE VULNOPS METRICS (REAL LIVE DATA) ---")
    print(f"[-] Vitesse de prise de décision : {metrics['triage_velocity_seconds']} secondes")
    print(f"[-] Vulnérabilités critiques totales : {metrics['total_critical_high_vulns']}")
    print(f"[-] Failles éligibles à l'auto-patching : {metrics['autonomous_eligible_vulns']}")
    print(f"[-] Taux d'absorption automatisé : {metrics['absorption_rate_percent']}%")
    print("[+] ---------------------------------------------------\n")
