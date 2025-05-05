import time
import signal
import sys
from .parser import update_table

def watch_tcp_connections(interval=4):
    """Continuously monitor TCP connections with live updating."""
    if interval <= 0:
        raise ValueError("Interval must be positive")

    def handle_interrupt(signum, frame):
        print("\nMonitoring stopped.")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_interrupt)

    while True:
        print("\033c", end="")  # Clear terminal
        table_lines = update_table()
        if table_lines:
            for line in table_lines:
                print(line)
        time.sleep(interval)
