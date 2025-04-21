import socket
import threading

# Set socket timeout
socket.setdefaulttimeout(1)

# List of common ports (for regular services)
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt"
}

# List of known exploit-targeted port ranges (examples)
EXPLOIT_PORT_RANGE = range(1337, 1400)  # example range used in CTFs/malware
EXPLOIT_PORTS = list(EXPLOIT_PORT_RANGE) + [6666, 6667, 6668, 31337]

# A variable to track whether any open ports were found
open_ports = []

# Threaded port scanning function
def scan_port(target, port, label):
    global open_ports
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            result = s.connect_ex((target, port))
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                print(f"[+] {label}: Port {port} OPEN ({service})")
                open_ports.append(port)
        except Exception as e:
            print(f"[!] {label}: Error scanning port {port} - {e}")

# Main scanner function
def smart_port_scanner(target):
    print(f"\n[*] Starting scan on {target}\n")

    try:
        # Scan common service ports
        print("[~] Scanning COMMON service ports...\n")
        for port in COMMON_PORTS:
            threading.Thread(target=scan_port, args=(target, port, "Common")).start()

        # Scan exploit-related ports
        print("\n[~] Scanning EXPLOIT-prone ports...\n")
        for port in EXPLOIT_PORTS:
            threading.Thread(target=scan_port, args=(target, port, "Exploit")).start()

    except socket.gaierror:
        print(f"[ERROR] Could not resolve target: {target}. Please check the IP/hostname.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    
    # Wait for threads to finish (this is important for the threading to work correctly)
    import time
    time.sleep(3)

    # Check if any open ports were found and display the result
    if not open_ports:
        print("[~] No open ports found.")
    else:
        print("\n[*] Open ports scan completed.")

# Script entry
if __name__ == "__main__":
    target_host = input("Enter IP or hostname to scan: ").strip()
    if target_host:
        smart_port_scanner(target_host)
    else:
        print("[ERROR] Invalid input. Please provide a valid IP or hostname.")