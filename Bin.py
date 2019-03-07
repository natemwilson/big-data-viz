import socket  # TODO: refactor using socketserver and handlers (maybe?)
import threading
import sys
import time
import datetime

class Bin:

    def __init__(self, size, type):
        self.type = type
        self.size = size
        self.count = [0]*size
        self.mean = [0]*size
        self.min = [sys.maxsize]*size
        self.max = [-sys.maxsize - 1]*size
        self.variance = [0]*size

    def update(self, record):



        if(self.type == 1):
            fmt = '%Y%m%d'
            s = str(record['UTC_DATE'])
            dt = datetime.datetime.strptime(s, fmt)
            tt = dt.timetuple()
            index = tt.tm_yday - 1
        else:
            index = int(str(record['UTC_DATE'])[4:6]) - 1
        self.count[index] += 1
        newVal = record['PRECIPITATION']
        self.max[index] = max(self.max[index],newVal)
        self.min[index] = min(self.min[index], newVal)
        mean = self.mean[index] + (newVal - self.mean[index]) / self.count[index]
        variance = self.variance[index] + (newVal - self.mean[index]) * (newVal - mean)
        self.mean[index] = mean
        self.variance[index] = variance
        # print("updating for index: " + str(index) + " where value is: " + str(newVal) + "count: " + str(self.count[index]))
        # print("new count: " + str(self.count))



