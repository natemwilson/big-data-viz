import socket  # TODO: refactor using socketserver and handlers (maybe?)
import threading
import sys
import time
import datetime

class Bin:

    def __init__(self):
        # self.type = type
        self.size = 5 # represent each of the 9 features
        self.count = 0
        self.mean = [0]*self.size
        self.min = [100000]*self.size
        self.max = [-1]*self.size
        self.variance = [0]*self.size

    def update(self, recordList):




        # AIR_TEMPERATURE = record['AIR_TEMPERATURE']
        # PRECIPITATION = record['PRECIPITATION']
        # SOLAR_RADIATION = record['SOLAR_RADIATION']
        # SURFACE_TEMPERATURE = record['SURFACE_TEMPERATURE']
        # RELATIVE_HUMIDITY = record['RELATIVE_HUMIDITY']

        self.count += 1

        self.max = [max(x1, x2) for x1, x2 in zip(self.max,recordList)]
        self.min = [min(x1, x2) for x1, x2 in zip(self.min, recordList)]

        for i in range(self.size):
            mean = self.mean[i] + (recordList[i] - self.mean[i]) / self.count
            variance = self.variance[i] + (recordList[i] - self.mean[i]) * (recordList[i] - mean)
            self.mean[i] = mean
            self.variance[i] = variance


        # print("updating for index: " + str(index) + " where value is: " + str(newVal) + "count: " + str(self.count[index]))
        # print("new count: " + str(self.count))



