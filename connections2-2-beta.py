import time
import signal
import os

# TCP state mapping with darker, dystopian colors
TCP_STATES = {
    '01': '\033[1;32;40mESTABLISHED\033[0m',  # Green on Black
    '02': '\033[1;31;40mSYN_SENT\033[0m',     # Red on Black
    '03': '\033[1;35;40mSYN_RECV\033[0m',     # Purple on Black
    '04': '\033[1;33;40mFIN_WAIT1\033[0m',    # Yellow on Black
    '05': '\033[1;38;5;214;40mFIN_WAIT2\033[0m', # Orange on Black
    '06': '\033[1;36;40mTIME_WAIT\033[0m',    # Cyan on Black
    '07': '\033[1;37;40mCLOSE\033[0m',        # White on Black
    '08': '\033[1;34;40mCLOSE_WAIT\033[0m',   # Blue on Black
    '09': '\033[1;35;40mLAST_ACK\033[0m',     # Magenta on Black
    '0A': '\033[1;30;47mLISTEN\033[0m',       # Black on White
    '0B': '\033[1;31;40mCLOSING\033[0m'       # Red on Black
}

def decode_state(state_hex):
    """Convert hex state to human-readable form with terminal colors."""
    return TCP_STATES.get(state_hex, state_hex)

def create_table():
    """Create a simple table format for output."""
    header = f"{'Protocol':<10} {'State':<20} {'Local Address:Port':<25} {'Peer Address:Port':<25}"
    separator = '-' * 80
    return header, separator

def get_tcp_connections():
    """Read and parse TCP connections from /proc/net/tcp."""
    try:
        with open('/proc/net/tcp', 'r') as file:
            return file.readlines()[1:]  # Skip header line
    except (FileNotFoundError, PermissionError) as e:
        print(f"\033[1;31;40mError: {e}\033[0m")  # Red text for errors
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
        local_ip, local_port = parts[1].split(':')
        peer_ip, peer_port = parts[2].split(':')
        
        local_ip = '.'.join(str(int(local_ip[i:i+2], 16)) for i in range(0, 8, 2))
        peer_ip = '.'.join(str(int(peer_ip[i:i+2], 16)) for i in range(0, 8, 2))
        
        line = f"{protocol:<10} {state:<20} {local_ip}:{int(local_port, 16):<25} {peer_ip}:{int(peer_port, 16):<25}"
        table_lines.append(line)
    
    return table_lines

def watch_tcp_connections(interval=4):
    """Continuously monitor TCP connections with live updating."""
    if interval <= 0:
        raise ValueError("Interval must be positive")
    
    def handle_interrupt(signum, frame):
        print("\n\033[1;33;40mMonitoring stopped.\033[0m")  # Yellow on Black for stop message
        exit(0)  # Exit cleanly on Ctrl+C
    
    signal.signal(signal.SIGINT, handle_interrupt)
    
    while True:
        os.system('clear')  # Clear terminal for each update (simulates live updates)
        table_lines = update_table()
        if table_lines:
            for line in table_lines:
                print(line)
        time.sleep(interval)

if __name__ == "__main__":
    try:
        print("\033[1;37;40mStarting TCP connection monitor (Ctrl+C to stop)...\033[0m")  # White on Black
        watch_tcp_connections(interval=4)
    except ValueError as e:
        print(f"\033[1;31;40m{e}\033[0m")  # Red on Black for errors
