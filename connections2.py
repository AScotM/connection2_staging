import time
import signal
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich import print

# TCP state mapping
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
    """Create and return a configured table."""
    table = Table(show_header=True, header_style="bold green", show_lines=True)
    table.add_column("Netid", style="bold blue", min_width=8)
    table.add_column("State", style="yellow", min_width=12)
    table.add_column("Local Address:Port", style="magenta", min_width=20)
    table.add_column("Peer Address:Port", style="cyan", min_width=20)
    return table

def get_tcp_connections():
    """Read and parse TCP connections from /proc/net/tcp."""
    try:
        with open('/proc/net/tcp', 'r') as file:
            return file.readlines()[1:]  # Skip header line
    except (FileNotFoundError, PermissionError) as e:
        print(f"[bold red]Error: {e}[/bold red]")
        return None

def update_table():
    """Generate an updated table with current TCP connections."""
    connections = get_tcp_connections()
    if not connections:
        return None
    
    table = create_table()
    
    for line in connections:
        parts = line.strip().split()
        if len(parts) < 4:
            continue
            
        netid = parts[0]
        state = decode_state(parts[3])
        
        # Convert address:port
        local_ip, local_port = parts[1].split(':')
        peer_ip, peer_port = parts[2].split(':')
        
        local_ip = '.'.join(str(int(local_ip[i:i+2], 16)) for i in range(0, 8, 2))
        peer_ip = '.'.join(str(int(peer_ip[i:i+2], 16)) for i in range(0, 8, 2))
        
        table.add_row(
            netid,
            state,
            f"{local_ip}:{int(local_port, 16)}",
            f"{peer_ip}:{int(peer_port, 16)}"
        )
    
    return table

def watch_tcp_connections(interval=4):
    """Continuously monitor TCP connections with live updating."""
    if interval <= 0:
        raise ValueError("Interval must be positive")
    
    def handle_interrupt(signum, frame):
        nonlocal running
        running = False
        print("\n[bold yellow]Monitoring stopped.[/bold yellow]")
    
    signal.signal(signal.SIGINT, handle_interrupt)
    running = True
    
    with Live(refresh_per_second=4, vertical_overflow="visible") as live:
        while running:
            table = update_table()
            if table:
                live.update(table)
            time.sleep(interval)

if __name__ == "__main__":
    try:
        print("[bold green]Starting TCP connection monitor (Ctrl+C to stop)...[/bold green]")
        watch_tcp_connections(interval=4)
    except ValueError as e:
        print(f"[bold red]{e}[/bold red]")
