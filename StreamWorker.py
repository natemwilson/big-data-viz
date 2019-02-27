import threading, struct


class StreamWorker(threading.Thread):

    def __init__(self, client_socket, address, index):
        super().__init__()
        self.client_socket = client_socket
        self.address = address
        self.index = index

    def run(self) -> None:
        with self.client_socket as sock:
            while True:
                # todo : consider adding exit conditions
                # todo : consider wrapping function contents with try except statement
                self.index['count'] += 1
                size_message, address = sock.recvfrom(4)
                size = struct.unpack('!I', size_message)[0]

                data_message, address = sock.recvfrom(size)

                print(f"size: {size}, msg: {data_message}")
