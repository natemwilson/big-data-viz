
class Rough():

    def __init__(self):
        super().__init__()
        self.index = 1

    def start(self):
        while self.index < 10:
            for x in range(4):
                if(self.index % (2 ** x) == 0):
                    print("model" + str(x+1) + " updated for " + str(self.index) )
            self.index += 1

if __name__ == '__main__':
        server = Rough()
        server.start()
