
from hosts import Host # from core/hosts take class Host
from hosts import load_hosts
import platform
from dataclasses import dataclass 
import subprocess
@dataclass 
class Ping: # create class for one ping
    destination: str
    ttl: int
    time: float
    transmitedPackets: int
    receivedPackets: int
    percentOfLossPackets: int


def ping_host(host:Host): # function to check connection
    systemOsFlag = "-c"
    if platform.system() == "Windows": # what is the system? Default is MacOS or Linux
        systemOsFlag = "-n"

    result = subprocess.run(["ping", systemOsFlag,"5",host.address], capture_output=True, text=True) # run subprocess to check connection
    lines = result.stdout.splitlines() #get block of text, and cut it to lines
    
  
    for line in lines:
        if "from" in line:
            parts = line.split() #cut line into pieces
            desitnation = parts[3]
            ttl = parts[5].split("=")[1]
            time = parts[6].split("=")[1]
            print("Time to kill:",ttl)
        elif "transmitted" in line:
            parts = line.split()
            transmitedPackets = parts[0]
            receivedPackets = parts[3]
            percentOfLossPackets = parts[5][:-1]
            print("Transmitted packets in shot: ",transmitedPackets)
host = load_hosts("../hosts.txt")
print(ping_host(host[3]))
