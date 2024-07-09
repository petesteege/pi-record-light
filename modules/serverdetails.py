import json
import os

PEER_DETAILS_FILE = 'peer_details.json'

def get_peer():
    """Retrieve peer details from the file."""
    if not os.path.exists(PEER_DETAILS_FILE):
        return None

    with open(PEER_DETAILS_FILE, 'r') as file:
        peer_details = json.load(file)
    return peer_details

def save_peer(ip_address, port_number, dns_name):
    """Save peer details to the file."""
    peer_details = {
        'ip_address': ip_address,
        'dns_name': dns_name,
        'port_number': port_number
    }

    with open(PEER_DETAILS_FILE, 'w') as file:
        json.dump(peer_details, file, indent=4)
