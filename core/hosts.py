#import packages
from dataclasses import dataclass, field
from pathlib import Path
import subprocess

#Begin coding
#Create class Host, which is responsible for one host from list
@dataclass
class Host:
 address: str #required address of host
 label: str = "" # nice to have label for this host, as it will give more info whose IP it is

 def display_name(self) -> str: #creating nice label, if not exist, then show ip address
    return self.label if self.label else self.address

def load_hosts(path: str | Path) ->list[Host]: # load hosts from file, and put them into list
    hosts = []
    filepath = Path(path)

    if not filepath.exists(): #If no hosts file was found, return error
        raise FileNotFoundError (f"No host file was found in: {filepath}")

    with filepath.open("r", encoding="utf-8") as openedHosts: # if it was possible to open hosts file, open it as OpenedHosts
        for line in openedHosts: #for each object(verse) in file
            line = line.strip() # remove white marks at the beginning and end of line

            if not line or line.startswith("#"): #if empty line (like enter) or its comment, ignore and go to next verse
                continue

            parts = line.split() #split line to words
            address = parts[0] #take first element of parts, and lock it in variable address
            label = parts[1] if len(parts) > 1 else ""
            hosts.append(Host(address=address, label=label))

    return hosts
