import socket
import socket

import concurrent.futures

def scan_ports(target, start_port, end_port):
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
        executor.map(scan_port, range(start_port, end_port + 1))

    return open_ports, closed_ports, filtered_ports

# Example usage
target_ip = "192.168.1.1"
start_port = 1
end_port = 65536

open_ports, closed_ports, filtered_ports = scan_ports(target_ip, start_port, end_port)
#Opciociones quicksan, fullscan, entre rangos de puertos y puertos especificos
print("Open ports:", open_ports)
print("Closed ports:", closed_ports)
print("Filtered ports:", filtered_ports)