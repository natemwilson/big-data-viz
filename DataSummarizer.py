import threading, struct, logging, queue, time

from Bin import Bin

class DataSummarizer(threading.Thread):

    def __init__(self,queueList):
        super().__init__()
        self.queueList = queueList
        self.index = 1
        self.bins = []

    def run(self):
        print("summarizer started")
        monthBin = Bin(12, 2)
        dayBin = Bin(365, 1)
        self.bins.append(dayBin)
        self.bins.append(monthBin)

        while True:
            while self.queueList.qsize() > 0:
                for x in range(len(self.bins)):
                    self.bins[x].update(self.queueList.get())

            time.sleep(1)

