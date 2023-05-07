import argparse
import csv
import socket
import threading
import time

def scan_ports(target_host, port_list, scan_type='tcp', timeout=1, banner_grab=False):
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
                
                # If banner_grab flag is set, attempt to grab the service banner
                if banner_grab:
                    try:
                        # Send a dummy request and receive the response
                        sock.sendall(b'\x00')
                        banner = sock.recv(1024)
                        
                        # If the response is not empty, print the banner
                        if banner:
                            print(f"Banner for {target_host}:{port}: {banner.decode().strip()}")
                            
                    except:
                        pass
            
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
    
    return (target_host, open_ports, closed_ports)

def scan_range(target_host, start_port, end_port, scan_type='tcp', timeout=1, banner_grab=False):
    # Convert start and end ports to integers
    start_port = int(start_port)
    end_port = int(end_port)
    
    # Generate the list of ports to scan
    port_list = list(range(start_port, end_port + 1))
    
    # Perform the port scan
    return scan_ports(target_host, port_list, scan_type, timeout, banner_grab)

def scan_hosts(targets, port_list, scan_type='tcp', timeout=1, banner_grab=False, output_file=None, input_file=None, num_threads=1):
    # Initialize list of results
    results = []
    
    # If an input file is specified, read the results and skip already scanned hosts
    if input_file:
        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] in targets:
                    targets.remove(row[0])
    
    # If there are no hosts left to scan, exit
if not targets:
    return results

# If num_threads is greater than the number of targets, reduce it to the number of targets
num_threads = min(num_threads, len(targets))

# Initialize a list of threads
threads = []

# Divide the targets among the threads
chunk_size = len(targets) // num_threads
chunks = [targets[i:i+chunk_size] for i in range(0, len(targets), chunk_size)]

# Create a thread for each chunk of targets
for i in range(num_threads):
    thread = threading.Thread(target=scan_chunk, args=(chunks[i], port_list, scan_type, timeout, banner_grab, output_file, input_file, results))
    threads.append(thread)
    
# Start the threads
for thread in threads:
    thread.start()
    
# Wait for the threads to finish
for thread in threads:
    thread.join()
    
# Sort the results by host
results.sort(key=lambda x: x[0])

# If an output file is specified, write the results to a CSV file
if output_file:
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)
        
return results
def scan_chunk(targets, port_list, scan_type, timeout, banner_grab, output_file, input_file, results):
# Loop through the targets and perform the port scan
for target in targets:
result = scan_ports(target, port_list, scan_type, timeout, banner_grab)
    # Add the result to the list of results
    results.append(result)
    
    # If an output file is specified, write the result to a CSV file
    if output_file:
        with open(output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(result)
            
    # If an input file is specified, write the result to the CSV file
    if input_file:
        with open(input_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(result)
            
    # Sleep for a short time to avoid overwhelming the target
    time.sleep(0.1)
if name == 'main':
# Parse command line arguments
parser = argparse.ArgumentParser(description='A simple port scanner for blue teamers')
parser.add_argument('targets', metavar='TARGET', nargs='+', help='the target(s) to scan')
parser.add_argument('-p', '--ports', metavar='PORT', help='the port(s) to scan (comma-separated or range, e.g. 1-1000)', default='1-65535')
parser.add_argument('-t', '--type', metavar='SCAN_TYPE', help='the type of scan to perform (tcp or udp)', default='tcp')
parser.add_argument('-T', '--timeout', metavar='TIMEOUT', type=int, help='the timeout (in seconds) for connection attempts', default=1)
parser.add_argument('-b', '--banner', action='store_true', help='perform a service banner grab on open ports')
parser.add_argument('-o', '--output', metavar='OUTPUT_FILE', help='output the scan results to a CSV file')
parser.add_argument('-i', '--input', metavar='INPUT_FILE', help='resume a previous scan from an input CSV file')
parser.add_argument('-n', '--threads', metavar='NUM_THREADS', type=int, help='the number of threads to use for scanning', default=1)
args = parser.parse_args()
# Parse the port
port_list = parse_ports(args.ports)
scan_type = args.type.lower()
timeout = args.timeout
banner_grab = args.banner
output_file = args.output
input_file = args.input
num_threads = args.threads

# If an input file is specified, resume the scan from the input file
if input_file:
    with open(input_file, 'r', newline='') as f:
        reader = csv.reader(f)
        results = [row for row in reader]
else:
    results = []

# Perform the port scan
scan_results = port_scan(args.targets, port_list, scan_type, timeout, banner_grab, output_file, input_file, results, num_threads)

# Print the results
print('Port Scan Results:')
print('------------------')
for result in scan_results:
    host = result[0]
    open_ports = result[1]
    closed_ports = result[2]
    filtered_ports = result[3]
    banners = result[4]
    
    print('Host: {}'.format(host))
    print('Open Ports: {}'.format(', '.join(str(port) for port in open_ports)))
    print('Closed Ports: {}'.format(', '.join(str(port) for port in closed_ports)))
    print('Filtered Ports: {}'.format(', '.join(str(port) for port in filtered_ports)))
    if banner_grab:
        for port, banner in banners.items():
            print('Banner for port {}: {}'.format(port, banner))
    print('')
    
print('Scan complete.')

