import socket

target_host = input("Enter the IP address of the target: ")
target_ports = input("Enter the ports to scan (separate with comma): ")

# Split the port list by comma and convert to integers
port_list = [int(port.strip()) for port in target_ports.split(",")]

# Loop through the ports and check if they're open
for port in port_list:
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a timeout of 1 second for the connection attempt
        sock.settimeout(1)
        
        # Attempt to connect to the target on the current port
        result = sock.connect_ex((target_host, port))
        
        # If the connection was successful, print the open port number
        if result == 0:
            print(f"Port {port} is open")
        
        # Close the socket
        sock.close()
        
    except KeyboardInterrupt:
        print("\nExiting due to user interrupt...")
        break
        
    except socket.gaierror:
        print("Hostname could not be resolved. Exiting...")
        break
        
    except socket.error:
        print("Couldn't connect to server. Exiting...")
        break
