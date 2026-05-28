#import packages
from core.hosts import load_hosts
from core.pinger import ping_host

#Begin coding

hosts = load_hosts("hosts.txt")
for host in hosts:
    print(f"\n---- {host.display_name()}({host.address})----")
    result = ping_host(host)
    for p in result:
        if p.error:
            print(f" | Connection impossible! Reason: {p.error}")
        else:
            print(f"{p.destination} | TTL: {p.ttl} | Time: {p.time}ms | Loss: {p.percentOfLossPackets}%")
