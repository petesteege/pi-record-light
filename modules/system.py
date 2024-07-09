import socket
import subprocess
import shared as shared

def get_ip():
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Connect to any remote server (does not send any data)
        sock.connect(("8.8.8.8", 80))
        
        # Get the local IP address bound to the socket
        local_ip = sock.getsockname()[0]
        
        return local_ip
    except socket.error:
        return None


def get_mac():
    try:
        # Run the shell command to get MAC address
        result = subprocess.check_output(["ifconfig", "-a"]).decode()
        for line in result.splitlines():
            if "ether " in line:
                mac_address = line.split("ether ")[1].strip().split()[0]
                return mac_address
        return None
    except Exception as e:
        print(f"Failed to retrieve MAC address: {e}")
        return None


def get_rtp():
    conf_file = shared.conf_file_path
    port_name = None
    try:
        with open(conf_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('alsa_name='):
                    port_name = line.split('=')[1].strip()
                    break
    except FileNotFoundError:
        print(f"Error: Configuration file {conf_file} not found.")
    except Exception as e:
        print(f"Error reading configuration file: {e}")
    
    return port_name



# SYSTEM ROUTINES


def shutdown():
    subprocess.run(['sudo', 'shutdown', 'now'])

def restart_app():
    subprocess.run(['sudo', 'systemctl', 'restart', 'recordlight.service'])

def reboot_sys():
    subprocess.run(['sudo', 'reboot'])