import socket
import threading

def handle_client_connection(client_socket):
    version = client_socket.recv(1)
    nmethods = client_socket.recv(1)
    methods = client_socket.recv(ord(nmethods))

    # Assume no authentication required
    client_socket.sendall(b'\x05\x00')  # SOCKS5 and no authentication

    # Get the request details
    version, cmd, _, atyp = client_socket.recv(4)
    if atyp == 1:  # IPv4
        address = socket.inet_ntoa(client_socket.recv(4))
    elif atyp == 3:  # Domain name
        domain_length = ord(client_socket.recv(1))
        address = client_socket.recv(domain_length)
    port = int.from_bytes(client_socket.recv(2), 'big')

    # Only handle CONNECT command
    if cmd == 1:  # CONNECT
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((address, port))
        client_socket.sendall(b'\x05\x00\x00\x01' + socket.inet_aton('0.0.0.0') + (1080).to_bytes(2, 'big'))

        # Forwarding loop
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            remote_socket.sendall(data)
            data = remote_socket.recv(4096)
            if not data:
                break
            client_socket.sendall(data)
    client_socket.close()
    remote_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 1080))  # Listen on all interfaces on port 1080
    server_socket.listen(5)
    print("SOCKS5 server listening on port 1080...")

    while True:
        client_sock, address = server_socket.accept()
        print(f'Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()

if __name__ == '__main__':
    main()
