import threading, struct, logging, queue, time

from Bin import Bin
from StreamCorrelationMatrix import StreamCorrelationMatrix


class DataSummarizer(threading.Thread):

    def __init__(self,queueList):
        super().__init__()
        self.queueList = queueList
        self.index = 1
        self.bins = []
        self.correlation_matrix = StreamCorrelationMatrix()


    def run(self):
        print("summarizer started")
        monthBin = Bin(12, 2)
        dayBin = Bin(365, 1)
        self.bins.append(dayBin)
        self.bins.append(monthBin)

        while True:
            while self.queueList.qsize() > 0:
                record = self.queueList.get()


                for bin in self.bins:
                    bin.update(record)


                self.correlation_matrix.update(record)

            time.sleep(1)

