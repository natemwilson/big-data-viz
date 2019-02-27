import socket  # TODO : refactor using socketserver and handlers (?)
import threading
from StreamWorker import StreamWorker


class AggregatorServer(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.streams = []
        self.index = {'count' : 0}
        self.host = host
        self.port = port

    def run(self):

        # consider starting up the Command Line Interpreter here?

        print(f"server listening on {self.host}:{self.port} ")
        with self.server_socket as s:
            s.listen()
            while True:
                client_socket, address = s.accept()
                print(f"connection opened by {address}")
                stream = StreamWorker(client_socket, address, self.index)
                self.streams.append(stream)
                stream.start()


if __name__ == '__main__':
    server = AggregatorServer('localhost', 5555)
    server.start()