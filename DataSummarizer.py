import threading, struct, logging, queue, time, sys, datetime

from Bin import Bin
from StreamCorrelationMatrix import StreamCorrelationMatrix
import numpy as np

import pygeohash as pgh
class DataSummarizer(threading.Thread):

    def __init__(self,queueList):
        super().__init__()
        self.queueList = queueList
        self.index = 1
        self.bins = []
        self.correlation_matrix = StreamCorrelationMatrix()

        self.geoHashList = set()
        self.featureMapping = {'AIR_TEMPERATURE':0,
                               'PRECIPITATION' :1,
                               'SOLAR_RADIATION' :2,
                               'SURFACE_TEMPERATURE' :3,
                               'RELATIVE_HUMIDITY' :4
                               }
        self.monthMapping = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def getMaxForDay(self, day, feature):
        return self.bins[0].get(day).max[self.featureMapping[feature]]

    def getMinForDay(self, day, feature):
        return self.bins[0].get(day).min[self.featureMapping[feature]]

    def getMeanForDay(self, day, feature):
        return self.bins[0].get(day).mean[self.featureMapping[feature]]

    def getVarianceForDay(self, day, feature):
        return self.bins[0].get(day).variance[self.featureMapping[feature]]

    def getUniqueLocation(self):
        return tuple(self.geoHashList)

    def get_start_end_day_for_month(self, month):
        startDay = 0
        if month is not 1:
            for i in range(month - 1):
                startDay += self.monthMapping[i]
        endDay = startDay + self.monthMapping[month - 1] - 1
        return startDay, endDay

    def getMinForMonth(self, month, feature):
        startDay, endDay = self.get_start_end_day_for_month(month)
        required_vals = []
        for i in range(startDay, endDay):
            value = self.getMinForDay(i, feature)
            print("value: " + str(value))
            if value != 100000 or int(value) != -9999:
                required_vals.append(value)
        if not required_vals:
            return -1
        min = np.min(required_vals)
        return min

    def getMinStatsByMonth(self, feature):

        list = []
        for i in range(1, 13):
            list.append(int(self.getMinForMonth(i, feature)))
        print("here in max stats by month feature: " + str(list))
        return list

    def getMaxForMonth(self, month, feature):
        startDay, endDay = self.get_start_end_day_for_month(month)
        required_vals = []
        for i in range(startDay, endDay):
            value = self.getMaxForDay(i, feature)
            if value != -1 or int(value) != -9999:
                required_vals.append(value)
        if not required_vals:
            return -1
        print("max req vals: " + str(required_vals))
        max = np.max(required_vals)
        print("for month: " + str(month) + "max: " + str(max))
        return max

    def getMaxStatsByMonth(self, feature):

        list = []
        for i in range(1, 13):
            print(i)
            list.append(int(self.getMaxForMonth(i, feature)))
        print("here in max stats by month feature: " + str(list))
        return list


    def getVarForMonth(self, month, feature):
        startDay, endDay = self.get_start_end_day_for_month(month)
        required_vals = []
        for i in range(startDay, endDay):
            required_vals.append(self.getVarianceForDay(i, feature))
        variance = np.var(required_vals)
        return variance

    def getvarStatsByMonth(self, feature):

        print("here in var stats by month feature: ")
        print(feature)
        list = []
        for i in range(1, 13):
            list.append(self.getVarForMonth(i, feature))
        return list
        # print(''.join(str(x) for x in list))
        # return ''.join((str(x) + "   ") for x in list)

    def getMeanStats(self, feature):
        print("here in mean stats feature: ")
        print(feature)
        list = []
        for key in self.bins[0].keys():
            print(str(self.bins[0].get(key)) + "  for key: " + str(key))
            print("value: " + str(self.bins[0].get(key).mean[self.featureMapping[feature]]))
            list.append(self.bins[0].get(key).mean[self.featureMapping[feature]])
        print(''.join(str(x) for x in list))
        return ''.join((str(x) + "   ") for x in list)
        # return list

    def getVarStats(self, feature):
        print("here in var stats feature: ")
        print(feature)
        list = []
        for key in self.bins[0].keys():
            print(str(self.bins[0].get(key)) + "  for key: " + str(key))
            print("value: " + str(self.bins[0].get(key).variance[self.featureMapping[feature]]))
            list.append(self.bins[0].get(key).variance[self.featureMapping[feature]])
        print(''.join(str(x) for x in list))
        return ''.join((str(x) + "   ") for x in list)

    def run(self):
        print("summarizer started")

        dayBin = {i : Bin() for i in range(366)}
        locationBin = {}
        self.bins.append(dayBin)
        self.bins.append(locationBin)

        while True:
            while self.queueList.qsize() > 0:
                record = self.queueList.get()

                featureList = ['AIR_TEMPERATURE', 'PRECIPITATION', 'SOLAR_RADIATION', 'SURFACE_TEMPERATURE',
                               'RELATIVE_HUMIDITY']
                recordList = [record[i] if int(record[i]) != -9999 else 0 for i in featureList]
                print(recordList)

                fmt = '%Y%m%d'
                s = str(record['UTC_DATE'])
                if s is '20180229':
                    continue
                dt = datetime.datetime.strptime(s, fmt)
                tt = dt.timetuple()
                nthDay = tt.tm_yday - 1
                dayBin[nthDay].update(recordList)

                lat = record['LATITUDE']
                long = record['LONGITUDE']
                geohash = pgh.encode(lat, long)
                if geohash in self.geoHashList:
                    locationBin[geohash].update(recordList)
                else:
                    newBin = Bin()
                    locationBin[geohash] = newBin
                    locationBin[geohash].update(recordList)
                    self.geoHashList.add(geohash)


                self.correlation_matrix.update(record)

            time.sleep(1)

