from .utils import decode_state

def get_tcp_connections():
    """Read and parse TCP connections from /proc/net/tcp."""
    try:
        with open('/proc/net/tcp', 'r') as file:
            return file.readlines()[1:]
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        return None

def create_table():
    """Create table headers."""
    header = f"{'Protocol':<10} {'State':<15} {'Local Address:Port':<25} {'Peer Address:Port':<25}"
    separator = '-' * 80
    return header, separator

def update_table():
    """Generate a table of TCP connections."""
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

        local_ip_hex, local_port = parts[1].split(':')
        peer_ip_hex, peer_port = parts[2].split(':')

        local_ip = '.'.join(str(int(local_ip_hex[i:i+2], 16)) for i in range(6, -2, -2))
        peer_ip = '.'.join(str(int(peer_ip_hex[i:i+2], 16)) for i in range(6, -2, -2))

        line = f"{protocol:<10} {state:<15} {local_ip}:{int(local_port, 16):<25} {peer_ip}:{int(peer_port, 16):<25}"
        table_lines.append(line)

    return table_lines
