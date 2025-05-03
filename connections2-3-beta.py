#!/usr/bin/env python3

import time
import signal
import sys

# TCP state mapping (plain text)
TCP_STATES = {
    '01': 'ESTABLISHED',
    '02': 'SYN_SENT',
    '03': 'SYN_RECV',
    '04': 'FIN_WAIT1',
    '05': 'FIN_WAIT2',
    '06': 'TIME_WAIT',
    '07': 'CLOSE',
    '08': 'CLOSE_WAIT',
    '09': 'LAST_ACK',
    '0A': 'LISTEN',
    '0B': 'CLOSING'
}

def decode_state(state_hex):
    """Convert hex state to human-readable form."""
    return TCP_STATES.get(state_hex, state_hex)

def create_table():
    """Create a simple table format for output."""
    header = f"{'Protocol':<10} {'State':<15} {'Local Address:Port':<25} {'Peer Address:Port':<25}"
    separator = '-' * 80
    return header, separator

def get_tcp_connections():
    """Read and parse TCP connections from /proc/net/tcp."""
    try:
        with open('/proc/net/tcp', 'r') as file:
            return file.readlines()[1:]  # Skip header line
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        return None

def update_table():
    """Generate an updated table with current TCP connections."""
    connections = get_tcp_connections()
    if not connections:
        return None
    
    header, separator = create_table()
    table_lines = [header, separator]
    
    for line in connections:
        parts = line.strip().split()
        if len(parts) < 4:
            continue

        protocol = "TCP"
        state = decode_state(parts[3])
        
        # Convert address:port
        local_ip_hex, local_port = parts[1].split(':')
        peer_ip_hex, peer_port = parts[2].split(':')

        local_ip = '.'.join(str(int(local_ip_hex[i:i+2], 16)) for i in range(6, -2, -2))
        peer_ip = '.'.join(str(int(peer_ip_hex[i:i+2], 16)) for i in range(6, -2, -2))

        line = f"{protocol:<10} {state:<15} {local_ip}:{int(local_port, 16):<25} {peer_ip}:{int(peer_port, 16):<25}"
        table_lines.append(line)
    
    return table_lines

def watch_tcp_connections(interval=4):
    """Continuously monitor TCP connections with live updating."""
    if interval <= 0:
        raise ValueError("Interval must be positive")
    
    def handle_interrupt(signum, frame):
        print("\nMonitoring stopped.")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, handle_interrupt)
    
    while True:
        print("\033c", end="")  # Clear terminal for each update (simple live update)
        table_lines = update_table()
        if table_lines:
            for line in table_lines:
                print(line)
        time.sleep(interval)

if __name__ == "__main__":
    try:
        print("Starting TCP connection monitor (Ctrl+C to stop)...")
        watch_tcp_connections(interval=4)
    except ValueError as e:
        print(f"Error: {e}")
