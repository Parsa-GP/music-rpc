import socket

class Server:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server is listening on {self.host}:{self.port}")

    def send(self, client_socket, message):
        client_socket.send(message.encode())
        #print(f"Sent: {message}")

    def receive(self, client_socket):
        data = client_socket.recv(655350).decode()
        #print(f"Received: {data}")
        return data

    def start(self, func):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")

            message = self.receive(client_socket)
            func(message)
        #client_socket.close()


class Client:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, message):
        self.client_socket.send(message.encode())
        #print(f"Sent: {message}")

    def receive(self):
        data = self.client_socket.recv(655350).decode()
        #print(f"Received: {data}")
        return data.decode('utf-8')

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def close(self):
        self.client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    server = True
    if server:
        server = Server()
        server.start()
    else:
        client = Client()
        client.connect()
        client.send("Hello from client!")
        client.receive()
        client.close()
