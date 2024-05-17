import socket
import threading

# Server settings
HOST = '192.168.209.242'
PORT = 12345

# List to keep track of connected clients
clients = []

def broadcast(message, client_socket=None):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Received: {message.decode('utf-8')}")
                broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on {HOST}:{PORT}")

    # Server can send messages
    def server_messages():
        while True:
            message = input("Server: ")
            broadcast(f"Server: {message}".encode('utf-8'))

    threading.Thread(target=server_messages).start()

    while True:
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
