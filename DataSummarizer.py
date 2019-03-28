import threading, struct, logging, queue, time, sys, datetime

from Bin import Bin
from StreamCorrelationMatrix import StreamCorrelationMatrix


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

    def getMaxForDay(self, day, feature):
        return self.bins[0].get(day).max[self.featureMapping[feature]]


    def run(self):
        print("summarizer started")
        # monthBin = Bin(12, 2)
        # dayBin = Bin(365, 1)

        dayBin = {i : Bin() for i in range(366)}
        locationBin = {}
        self.bins.append(dayBin)
        self.bins.append(locationBin)

        while True:
            while self.queueList.qsize() > 0:
                record = self.queueList.get()

                featureList = ['AIR_TEMPERATURE', 'PRECIPITATION', 'SOLAR_RADIATION', 'SURFACE_TEMPERATURE',
                               'RELATIVE_HUMIDITY']
                recordList = [record[i] for i in featureList]


                fmt = '%Y%m%d'
                s = str(record['UTC_DATE'])
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

                print("record: " + str(recordList))
                print("max of air temperture: " + str(locationBin[geohash].max))

                # for bin in self.bins:
                #     bin.update(record)



                self.correlation_matrix.update(record)

            time.sleep(1)

