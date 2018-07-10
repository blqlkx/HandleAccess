import sys
import os
from datetime import datetime
# from HandleMeoAccess import *

DATA_PATH = "DATA"
SAVED_FILE = "SelectedSources.txt"








def HandleSelectedSources(f):

    pass









def HandleSLinks(SatelliteOrignalLinks):
    SingleItems = []
    for SingleSatelliteOrignalLinks in SatelliteOrignalLinks:
        for SingleSchedSLinks in SingleSatelliteOrignalLinks:
            SingleItems.append(SingleSchedSLinks)
    return SingleItems

def HandleLine(rec):


    # line = f.readline()
    # SingleSatelliteLinks = []
    # while line:
    #
    #     if line.startswith("Global Statistics"):
    #         for i in range(7):
    #             f.readline()
    #     if line.startswith("MEO") or line.startswith("LEO") or line.startswith("GEO"):
    #         nodes = line.split("-To-")
    #         f.readline()
    #         f.readline()
    #         f.readline()
    #
    #         if line.startswith("Min Elevation"):
    #             for i in range(6):
    #                 f.readline()
    #
    #
    #         records = []
    #         line = f.readline()
    #         while len(line) > 2:
    #             records.append(line)
    #             line = f.readline()
    #         SingleSatelliteLinks.append(HandleSingleRecords(nodes, records))
    #     else:
    #         if not line:
    #             break
    #         line = f.readline()
    # return SingleSatelliteLinks

    pass




if __name__ == "__main__":
    files = os.listdir(DATA_PATH)
    os.chdir(DATA_PATH)
    for file in files:
        if file.endswith("Sources.txt"):
            f = open(file,'r')
            HandleSelectedSources(f)
            f.close()
            #print(file)