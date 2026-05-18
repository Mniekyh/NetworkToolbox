
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


def ping_host(host:Host): # function to check connection
    systemOsFlag = "-c"
    if platform.system() == "Windows": # what is the system? Default is MacOS or Linux
        systemOsFlag = "-n"

    result = subprocess.run(["ping", systemOsFlag,"5",host.address], capture_output=True, text=True) # run subprocess to check connection
            lines = result.stdout.splitlines() #get block of text, and cut it to lines

            if not lines or lines.startswith("#"): #if comment or empty line, continue
                continue

            parts = lines.split() #cut line into pieces
            desitnation = parts[0]
            ttl = 
