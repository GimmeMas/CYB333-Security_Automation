import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))		#connection
        print(f"[CLIENT] Connected to server at {HOST}:{PORT}")		#message showing connection
        
        while True:
            message = input("[CLIENT]: ")
            if message.lower() == 'exit':		#if condition showing option to exit
                print("[CLIENT] Closing connection.")
                break
            client_socket.sendall(message.encode())

            data = client_socket.recv(1024)
            if not data:
                print("[CLIENT] Server closed the connection.")
                break
            print(f"[SERVER]: {data.decode()}")

if __name__ == "__main__":
    start_client()