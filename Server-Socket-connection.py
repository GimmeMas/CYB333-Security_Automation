import socket
import sys

HOST = '127.0.0.1'
PORT = 12345
INACTIVITY_TIMEOUT = 60  # seconds (adjust as needed)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse address
        try:
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f"[SERVER] Listening on {HOST}:{PORT}")
        except Exception as e:
            print(f"[SERVER ERROR] Could not start server: {e}")
            sys.exit(1)

        try:
            server_socket.settimeout(INACTIVITY_TIMEOUT)
            conn, addr = server_socket.accept()
            conn.settimeout(INACTIVITY_TIMEOUT)
            with conn:
                print(f"[SERVER] Connected by {addr}")
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            print("[SERVER] Client disconnected.")
                            break
                        message = data.decode()
                        print(f"[CLIENT]: {message}")

                        response = input("[SERVER]: ")
                        conn.sendall(response.encode())
                    except socket.timeout:
                        print("[SERVER] Connection timed out due to inactivity.")
                        conn.sendall(b"Disconnected: Server timed out.")
                        break
                    except Exception as e:
                        print(f"[SERVER ERROR] {e}")
                        break
        except socket.timeout:
            print(f"[SERVER] No incoming connections after {INACTIVITY_TIMEOUT} seconds. Shutting down.")
        except Exception as e:
            print(f"[SERVER ERROR] {e}")

if __name__ == "__main__":
    start_server()