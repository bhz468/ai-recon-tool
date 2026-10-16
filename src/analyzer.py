import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"

def analyze_scan(scan_data):
    prompt = f"""Tu es un expert en pentest qui analyse des résultats de scan Nmap.

Résultats du scan :
{json.dumps(scan_data, indent=2)}

Pour CHAQUE port ouvert, réponds en suivant EXACTEMENT ce format, en étant spécifique au service (ne répète pas la même phrase générique pour chaque port) :

Port [numéro] ([service]) :
- Contexte : qu'est-ce que ce service fait normalement sur ce type de machine ?
- Risque réel : un risque concret et plausible, PAS une formule générique type "peut permettre de prendre le contrôle"
- Action concrète : une commande ou vérification précise (ex: nom d'outil réel, nom de CVE connu si pertinent, ou configuration à vérifier)

Si un service est mal identifié par Nmap (ex: tcpwrapped) ou si c'est un faux positif probable, dis-le clairement plutôt que d'inventer un risque."""

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"]

if __name__ == "__main__":
    with open('reports/scan_result.json', 'r') as f:
        scan_data = json.load(f)

    print("Analyse en cours avec Ollama (peut prendre 20-60 secondes sur CPU)...\n")
    analysis = analyze_scan(scan_data)
    print(analysis)

    with open('reports/analysis.txt', 'w') as f:
        f.write(analysis)
