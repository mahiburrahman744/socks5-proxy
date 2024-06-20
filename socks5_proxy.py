import socket
import threading
import time
import random

current_port = None  # Global variable to hold the current port

def run_proxy_server():
    global current_port
    while True:
        port = random.randint(1025, 65535)
        current_port = port  # Update the global variable
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server_socket.bind(('0.0.0.0', port))
            server_socket.listen(1)
            print(f"Listening on port {port}")
            
            server_socket.settimeout(1)  # Timeout for accept() to trigger every second
            
            try:
                while True:
                    client_socket, addr = server_socket.accept()
                    print(f"Accepted connection from {addr}")
                    client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
                    client_thread.start()
            except socket.timeout:
                pass
        except Exception as e:
            print(f"Failed to bind to port {port}: {e}")
        finally:
            server_socket.close()
        time.sleep(1)  # Ensure the port changes every second

def handle_client_connection(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            client_socket.send(data)
    finally:
        client_socket.close()

threading.Thread(target=run_proxy_server).start()
