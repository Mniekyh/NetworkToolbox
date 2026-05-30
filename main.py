#import packages
from core.hosts import load_hosts
from core.pinger import ping_host
from core.pinger import ping_all

#Begin coding
#use function from hosts.py, and do dictionary from it
hosts = load_hosts("hosts.txt")
results = ping_all(hosts) # ping all hosts from hosts.txt to check connection info
    
for host,pings in results.items(): #handle dictionary which U got

    print(f"\n---- {host.display_name()}({host.address})----" #Call name of pinged host
    for p in pings:
        if p.error: #if U get no connection, highlight it, and tell what is the problem
            print(f" | Connection impossible! Reason: {p.error}")
        else:#ion other case, show us info about connection
            print(f"{p.destination} | TTL: {p.ttl} | Time: {p.time}ms | Loss: {p.percentOfLossPackets}%")
