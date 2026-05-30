#import packages
from core.hosts import load_hosts
from core.pinger import ping_host
from core.pinger import ping_all

#Begin coding

hosts = load_hosts("hosts.txt")
results = ping_all(hosts)
    
for host,pings in results.items():

    print(f"\n---- {host.display_name()}({host.address})----")
    for p in pings:
        if p.error:
            print(f" | Connection impossible! Reason: {p.error}")
        else:
            print(f"{p.destination} | TTL: {p.ttl} | Time: {p.time}ms | Loss: {p.percentOfLossPackets}%")
