import socket  # TODO: refactor using socketserver and handlers (maybe?)
import threading, queue
import sys
import time
from StreamWorker import StreamWorker

from Summarizer import Summarizer


class AggregatorServer(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.streams = []  # todo: implement logic for removing dead streams from this list
        self.host = host
        self.port = port
        self.index = {'records_observed': 0, 'connections_made': 0}
        self.start_time = time.time()
        self.queueList = queue.Queue()
        self.summarizer = Summarizer(self.queueList)

    def run(self):

        # consider starting up the Command Line Interpreter here?

        print(f"server listening on {self.host}:{self.port}\n")
        with self.server_socket as s:
            s.listen()

            self.summarizer.start()
            while True:
                client_socket, address = s.accept()
                print(f"connection opened by {address}")
                self.index['connections_made'] += 1
                stream = StreamWorker(client_socket, address, self.index, self.queueList)

                self.streams.append(stream)
                stream.start()

    def start_interpreter(self):
        alive = True

        while alive:
            print("> ", end='')
            line = input()
            command = line.split(" ", 1)[0]

            if command == "ls":
                [print(stream, stream.is_alive()) for stream in self.streams]
            elif command == 'info':
                print(f"aggregator server started {self.start_time}")
                print(f"{self.index['connections_made']} connections opened.")
                print(f"{self.index['records_observed']} records processed.")
            elif command == 'exit':
                print('goodbye')
                sys.exit(0)
            elif command == 'help':
                print('print help message') # todo: write this up
            elif command == 'getCount':
                print(str(self.summarizer.getStatsCount()))
            elif command == 'getMax':
                # print("".join(["\t\t\t\t" + str(i) for i in range(7)]))
                for i, model in enumerate(self.summarizer.models):
                    for item in model.max:
                        print(f"{item:.2f}\t\t", end='')
                    print()
            elif command == 'getMin':
                for i, model in enumerate(self.summarizer.models):
                    for item in model.min:
                        print(f"{item:.2f}\t\t", end='')
                    print()
            elif command == 'getMean':
                for i, model in enumerate(self.summarizer.models):
                    for item in model.mean:
                        print(f"{item:.2f}\t\t", end='')
                    print()
            elif command == 'getVariance':
                for i, model in enumerate(self.summarizer.models):
                    for item in model.variance:
                        print(f"{item:.2f}\t\t", end='')
                    print()
            elif command == 'corr':
                a1 = line.split(" ")[1]
                a2 = line.split(" ")[2]
                print(self.summarizer.correlation_matrix.get_correlation(a1, a2))

            else:
                print(f"command: {command} not supported. try help")

if __name__ == '__main__':
    server = AggregatorServer('localhost', 5555)
    server.start()
    server.start_interpreter()