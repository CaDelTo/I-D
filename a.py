import socket
import socket

import concurrent.futures

def scan_ports(target, ports):
    open_ports = []
    closed_ports = []
    filtered_ports = []

    def scan_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target, port))

        if result == 0:
            open_ports.append(port)
        elif result == 11:
            filtered_ports.append(port)
        else:
            closed_ports.append(port)

        sock.close()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scan_port, ports)

    return open_ports, closed_ports, filtered_ports

# Example usage


commonPorts = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]

ip = input('Enter target IP: ')
opc = input('Select an option:\n1. Quickscan (Common Ports)\n2. Fullscan (Ports 1-65536)\n3.Range\n4.Specific Port\nEnter option:')
if opc == '1':
    ports = commonPorts
elif opc == '2':
    print('Scanning all ports (1-65536) This may take a while...')
    ports = list(range(1, 65537))
elif opc == '3':   
    start_port = int(input('Enter start port: '))
    end_port = int(input('Enter end port: '))
    port = list(range(start_port, end_port+1))
elif opc == '4':
    start_port = int(input('Enter port: '))
    ports = [start_port]
else:
    print('Invalid option')
    exit()
print('Scanning...')
open_ports, closed_ports, filtered_ports = scan_ports(ip, ports)
print("Open ports:", open_ports)
print("Closed ports:", closed_ports)
print("Filtered ports:", filtered_ports)