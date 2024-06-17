import socket
import threading
from typing import List

class Server:
    def __init__(self, port):
        self.port = port
        self.clients: List[socket.socket] = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_client(self, cl_sock: socket.socket):
        while True:
            try:
                msg = cl_sock.recv(1024)
                if not msg:
                    break
                print(msg.decode('utf-8'))
                self.broadcast_message(msg, cl_sock)
            except ConnectionResetError:
                break
            except Exception as e:
                print(f'Error handling client {cl_sock.getpeername()}: {e}')
                break
        self.remove_client(cl_sock)

    def broadcast_message(self, msg: bytes, source_sock: socket.socket):
        for cl in self.clients[:]:
            if cl is not source_sock:
                try:
                    cl.sendall(msg)
                except Exception as e:
                    print(f'Error sending message to {cl.getpeername()}: {e}')
                    self.remove_client(cl)

    def remove_client(self, cl_sock: socket.socket):
        if cl_sock in self.clients:
            self.clients.remove(cl_sock)
            try:
                cl_sock.close()
            except Exception as e:
                print(f'Error closing socket {cl_sock.getpeername()}: {e}')
            print(f'Client {cl_sock.getpeername()} disconnected')

    def setup_server(self):
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ip = '10.112.40.223'
        self.server.bind((ip, self.port))
        print(f'Listening on {ip} port {self.port}')
        self.server.listen(10)

    def accept_connections(self):
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            print(f'User {addr} connected')
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()

    def start(self):
        self.setup_server()
        self.accept_connections()

if __name__ == '__main__':
    x = Server(port=53773)
    x.start()
