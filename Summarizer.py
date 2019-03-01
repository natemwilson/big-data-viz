import threading, struct, logging, queue, time

from Model import Model

class Summarizer(threading.Thread):

    def __init__(self,queueList):
        super().__init__()
        self.queueList = queueList
        self.index = 1
        self.models = []

    def run(self):
        print("summarizer started")
        model1 = Model(1)
        model2 = Model(2)
        model3 = Model(4)
        model4 = Model(8)
        self.models.extend([model1,model2,model3,model4])

        while True:
            while self.queueList.qsize() > 0:
                for x in range(4):
                    if(self.index % (2 ** x) == 0):
                        # print(str(self.queueList.get().values()))
                        self.models[x].update(self.queueList.get())
                self.index += 1
            time.sleep(1)
            # print("q size = " + str(self.queueList.qsize()))

    def getStatsCount(self):
        list = []
        for x in range(4):
            list.append(self.models[x].getCount())
        return list

    def getStatsMax(self):
        list = []
        for x in range(4):
            list.append(self.models[x].getMax())
        return list

    def getStatsMin(self):
        list = []
        for x in range(4):
            list.append(self.models[x].getMin())
        return list

# if __name__ == '__main__':
#     q = queue.Queue()
#     q.put(1)
#     q.put(2)
#     summarizer = Summarizer(q)
#     summarizer.summarize()
