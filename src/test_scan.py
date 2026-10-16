import nmap

scanner = nmap.PortScanner()
print("Scan en cours sur localhost...")
scanner.scan('127.0.0.1', arguments='-sV -T4')

for host in scanner.all_hosts():
    print(f"\nHôte : {host} ({scanner[host].hostname()})")
    print(f"État : {scanner[host].state()}")
    for proto in scanner[host].all_protocols():
        ports = scanner[host][proto].keys()
        for port in sorted(ports):
            service = scanner[host][proto][port]
            print(f"  Port {port}/{proto} : {service['state']} - {service['name']} {service.get('version', '')}")
