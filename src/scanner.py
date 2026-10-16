import nmap
import json
from datetime import datetime

def scan_target(target, arguments='-sV -T4'):
    scanner = nmap.PortScanner()
    scanner.scan(target, arguments=arguments)

    results = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "hosts": []
    }

    for host in scanner.all_hosts():
        host_data = {
            "ip": host,
            "hostname": scanner[host].hostname(),
            "state": scanner[host].state(),
            "ports": []
        }
        for proto in scanner[host].all_protocols():
            for port in sorted(scanner[host][proto].keys()):
                service = scanner[host][proto][port]
                host_data["ports"].append({
                    "port": port,
                    "protocol": proto,
                    "state": service['state'],
                    "service": service['name'],
                    "version": service.get('version', ''),
                    "product": service.get('product', '')
                })
        results["hosts"].append(host_data)

    return results

if __name__ == "__main__":
    data = scan_target('127.0.0.1')
    with open('reports/scan_result.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(json.dumps(data, indent=2))
