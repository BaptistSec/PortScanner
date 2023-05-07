import argparse
import socket

def scan_ports(target_host, port_list, scan_type='tcp', timeout=1):
    # Initialize counters for open and closed ports
    open_ports = []
    closed_ports = []
    
    # Loop through the ports and check if they're open
    for port in port_list:
        try:
            # Create a socket object
            if scan_type == 'tcp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif scan_type == 'udp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                print("Invalid scan type. Exiting...")
                return
            
            # Set a timeout for the connection attempt
            sock.settimeout(timeout)
            
            # Attempt to connect to the target on the current port
            result = sock.connect_ex((target_host, port))
            
            # If the connection was successful, add the port to the open_ports list
            if result == 0:
                open_ports.append(port)
            
            # If the connection was unsuccessful, add the port to the closed_ports list
            else:
                closed_ports.append(port)
            
            # Close the socket
            sock.close()
            
        except KeyboardInterrupt:
            print("\nExiting due to user interrupt...")
            return
            
        except socket.gaierror:
            print(f"Hostname '{target_host}' could not be resolved. Exiting...")
            return
            
        except socket.error as e:
            print(f"Error connecting to port {port}: {e}")
            return
    
    # Print summary message with number of open and closed ports
    print(f"\nScan results for {target_host}:")
    print(f"  {len(open_ports)} open port(s): {open_ports}")
    print(f"  {len(closed_ports)} closed port(s): {closed_ports}")

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Simple port scanner for Blue Teamers')
    parser.add_argument('target', type=str, help='Target IP address or hostname')
    parser.add_argument('ports', type=str, help='Comma-separated list of ports to scan')
    parser.add_argument('--timeout', type=int, default=1, help='Scan timeout in seconds (default: 1)')
    parser.add_argument('--udp', action='store_true', help='Perform UDP port scan (default: TCP)')
    args = parser.parse_args()
    
    # Split the port list by comma and convert to integers
    port_list = [int(port.strip()) for port in args.ports.split(",")]
    
    # Perform the port scan
    if args.udp:
        scan_type = 'udp'
    else:
        scan_type = 'tcp'
    
    scan_ports(args.target, port_list, scan_type, args.timeout)
