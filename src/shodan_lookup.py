import os
import shodan
from dotenv import load_dotenv

load_dotenv()

def lookup_ip(ip):
    api_key = os.getenv('SHODAN_API_KEY')
    api = shodan.Shodan(api_key)
    try:
        result = api.host(ip)
        return {
            "ip": result.get('ip_str'),
            "org": result.get('org', 'N/A'),
            "os": result.get('os', 'N/A'),
            "ports": result.get('ports', []),
            "vulns": list(result.get('vulns', []))
        }
    except shodan.APIError as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Shodan n'indexe que des IP publiques, 127.0.0.1 ne fonctionnera pas ici
    result = lookup_ip("8.8.8.8")
    print(result)
