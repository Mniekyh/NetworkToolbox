
from core.hosts import Host # from core/hosts take class Host
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
    error: str = None

def whatSystemInUse():
  #I should create smaller function for this check, losing resources on this :/
    systemOsFlag = "-c" #("System in use: Linux/Unix")
    if platform.system() == "Windows": # what is the system? Default is MacOS or Linux
        systemOsFlag = "-n" #("System in use: Windows")
    return(systemOsFlag)

def ping_host(host:Host): # function to check connection
    systemOsFlag = whatSystemInUse()
    result = subprocess.run(["ping", systemOsFlag,"5",host.address], capture_output=True, text=True) # run subprocess to check connection
    #check if connection exist
    if result.returncode != 0:
    # noConnectioun
        #print(f"DEBUG stderr: '{result.stderr}'")
       #print(f"DEBUG stdout: '{result.stdout}'")
        return [Ping(
        destination=host.address,
        ttl=0,
        time=0.0,
        transmitedPackets=0,
        receivedPackets=0,
        percentOfLossPackets=0,
        error=result.stdout
    )]

    lines = result.stdout.splitlines() #get block of text, and cut it to lines
    pings = []
    transmitedPackets = 0
    receivedPackets = 0
    percentOfLossPackets = 0
  
    for line in lines:
        if "from" in line:
            parts = line.split()
            destination = host.address
            ttl = 0
            time = 0.0
            for part in parts:
                if part.startswith("ttl="):
                    ttl = int(part.split("=")[1])
                if part.startswith("time="):
                    time = float(part.split("=")[1])
            pings.append(Ping(
                destination=destination,
                ttl=ttl,
                time=time,
                transmitedPackets=0,
                receivedPackets=0,
                percentOfLossPackets=0
            ))
        elif "transmitted" in line:
            parts = line.split()
            transmitedPackets = int(parts[0])
            receivedPackets = int(parts[3])
            percentOfLossPackets = int(parts[5][:-1])
    # wpisz statystyki do każdego pinga
    for ping in pings:
        ping.transmitedPackets = transmitedPackets
        ping.receivedPackets = receivedPackets
        ping.percentOfLossPackets = percentOfLossPackets

    return pings
