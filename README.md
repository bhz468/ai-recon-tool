# AI-Powered Recon Tool

Automatise la reconnaissance réseau en pentest : scan Nmap, enrichissement Shodan (IP publiques), analyse par LLM local (Ollama) pour générer des pistes d'investigation.

## Stack
- Nmap (scan de ports et services)
- Shodan API (enrichissement d'IP publiques : organisation, OS, vulnérabilités connues)
- Ollama + Llama 3.2 3B (analyse IA en local, gratuit, sans clé API externe)

## Utilisation
```bash
# Cible locale/privée (Shodan ignoré automatiquement)
python3 src/main.py 127.0.0.1

# Cible publique (active le lookup Shodan)
python3 src/main.py scanme.nmap.org --public
```

## ⚠️ Usage éthique
Ne scanner que des machines que vous possédez ou pour lesquelles vous avez une autorisation explicite. `scanme.nmap.org` est un serveur mis à disposition par le projet Nmap pour les tests.

## Limites connues
- Le modèle local (3B paramètres) peut halluciner des noms d'outils ou mal interpréter certains statuts Nmap (ex: confondre "tcpwrapped" avec un vrai service, ou générer des recommandations génériques). L'outil sert à accélérer le triage initial, une validation humaine reste nécessaire.
- Shodan ne couvre que les IP publiques déjà indexées par leurs robots.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2:3b
```
Créer un fichier `.env` avec `SHODAN_API_KEY=votre_cle` (clé gratuite sur shodan.io).
