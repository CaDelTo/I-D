import ipaddress

import socket, concurrent.futures

def scan_ports(target, ports):
    """
    Scan the specified ports on the target IP address or domain name.

    Args:
        target (str): The target IP address or domain name to scan.
        ports (list): A list of ports to scan.

    Returns:
        tuple: A tuple containing three lists - open_ports, closed_ports, and filtered_ports.
            - open_ports: A list of open ports on the target IP address or domain name.
            - closed_ports: A list of closed ports on the target IP address or domain name.
            - filtered_ports: A list of filtered ports on the target IP address or domain name.
    """
    open_ports = []
    closed_ports = []
    filtered_ports = []

    def scan_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            elif result == 11:
                filtered_ports.append(port)
            else:
                closed_ports.append(port)
        except socket.gaierror:
            print('Invalid target')
        finally:
            sock.close()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scan_port, ports)

    return open_ports, closed_ports, filtered_ports

commonPorts = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]

while True:
    print('-'*60)
    target = input('Enter target IP or domain name: ')
    try:
        ipaddress.ip_address(target)
    except ValueError:
        try:
            ipaddress.ip_address(socket.gethostbyname(target))
        except socket.gaierror:
            print('Invalid target')
            continue
    opc = input('Select an option:\n1. Quickscan (Most Common Ports)\n2. Fullscan (Ports 1-65536)\n3. Range (From a to b)\n4. Specific Port\nEnter option: ')
    if opc == '1':
        ports = commonPorts
    elif opc == '2':
        print('Scanning all ports (1-65536) This may take a while...')
        ports = list(range(1, 65537))
    elif opc == '3':   
        start_port = int(input('Enter start port: '))
        end_port = int(input('Enter end port: '))
        ports = list(range(start_port, end_port+1))
    elif opc == '4':
        start_port = int(input('Enter port: '))
        ports = [start_port]
    else:
        print('Invalid option')
        continue
    print('\nScanning...')
    open_ports, closed_ports, filtered_ports = scan_ports(target, ports)
    print('-'*60)
    print("Scan complete!")
    print('Results:')
    print("Open ports:", open_ports)
    print("Closed ports:", closed_ports)
    print("Filtered ports:", filtered_ports)
    print('-'*60)
    print('Do you want to scan another target?')
    opc = input('Enter y/n: ')
    if opc != 'y':
        break
