import socket
import subprocess
import sys
from datetime import datetime

import concurrent.futures

subprocess.call('clear', shell=True)

remoteServer = input("Enter a remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)

print("-" * 60)
print("Please wait, scanning remote host", remoteServerIP)
print("-" * 60)

t1 = datetime.now()

def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((remoteServerIP, port))
    if result == 0:
        print("Port {}: Open".format(port))
    sock.close()

try:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scan_port, range(1, 1025))

except KeyboardInterrupt:
    print("You pressed Ctrl+C")
    sys.exit()
except socket.gaierror:
    print("Hostname could not be resolved. Exiting")
    sys.exit()
except socket.error:
    print("Couldn't connect to server")
    sys.exit()

t2 = datetime.now()
total = t2 - t1

print("Scanning completed in:", total)