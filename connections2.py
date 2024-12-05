import time
from rich.console import Console
from rich.table import Table
from rich.color import Color

def read_tcp_connections():
    console = Console()
    
    # Create a table for structured output
    table = Table(show_header=True, header_style="bold green", show_lines=True)
    table.add_column("Netid", style="bold blue")
    table.add_column("State", style="yellow")
    table.add_column("Local Address:Port", style="magenta")
    table.add_column("Peer Address:Port", style="cyan")
    
    try:
        with open('/proc/net/tcp', 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:  # Skip the first line (headers)
                line_data = line.split()
                # Extract relevant information
                netid = line_data[0]
                local_address, local_port = line_data[1].split(':')
                peer_address, peer_port = line_data[2].split(':')
                state = line_data[3]
                # Convert addresses from hex to IP format
                local_address = '.'.join(str(int(local_address[i:i + 2], 16)) for i in range(0, 8, 2))
                peer_address = '.'.join(str(int(peer_address[i:i + 2], 16)) for i in range(0, 8, 2))
                
                # Add rows to the table
                table.add_row(
                    netid, 
                    state, 
                    f"{local_address}:{int(local_port, 16)}", 
                    f"{peer_address}:{int(peer_port, 16)}"
                )
                
        console.print(table)
    
    except Exception as e:
        console.print(f"[bold red]Error reading /proc/net/tcp: {e}[/bold red]")

def watch_tcp_connections(interval):
    while True:
        read_tcp_connections()
        time.sleep(interval)

if __name__ == "__main__":
    # Specify the interval in seconds
    interval = 2  # Change this to your desired interval
    watch_tcp_connections(interval)

