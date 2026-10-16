import sys
import json
import os
import socket
from scanner import scan_target
from analyzer import analyze_scan
from shodan_lookup import lookup_ip

# Chemin absolu vers la racine du projet, peu importe d'où le script est lancé
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')

def run_recon(target, is_public_ip=False):
    print(f"[1/3] Scan Nmap sur {target}...")
    scan_data = scan_target(target)

    shodan_data = None
    if is_public_ip:
        try:
            resolved_ip = socket.gethostbyname(target)
            print(f"[2/3] Lookup Shodan sur {target} ({resolved_ip})...")
            shodan_data = lookup_ip(resolved_ip)
            scan_data["shodan"] = shodan_data
        except socket.gaierror:
            print(f"[2/3] Impossible de résoudre {target} en IP — Shodan ignoré")
    else:
        print("[2/3] IP privée/locale — Shodan ignoré (ne couvre que les IP publiques)")

    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(os.path.join(REPORTS_DIR, 'scan_result.json'), 'w') as f:
        json.dump(scan_data, f, indent=2)

    print("[3/3] Analyse IA en cours (peut prendre 30-90s sur CPU)...")
    analysis = analyze_scan(scan_data)

    with open(os.path.join(REPORTS_DIR, 'analysis.txt'), 'w') as f:
        f.write(analysis)

    print("\n=== RAPPORT DE RECONNAISSANCE ===\n")
    print(analysis)
    print(f"\nRapport complet sauvegardé dans reports/analysis.txt")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/main.py <ip_ou_domaine> [--public]")
        sys.exit(1)

    target = sys.argv[1]
    is_public = "--public" in sys.argv
    run_recon(target, is_public_ip=is_public)

