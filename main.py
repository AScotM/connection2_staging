from monitor.core import watch_tcp_connections

if __name__ == "__main__":
    try:
        print("Starting TCP connection monitor (Ctrl+C to stop)...")
        watch_tcp_connections(interval=4)
    except ValueError as e:
        print(f"Error: {e}")

