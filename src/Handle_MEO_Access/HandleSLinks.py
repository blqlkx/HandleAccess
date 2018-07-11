import sys
import os
from operator import itemgetter, attrgetter
from HandleMeoAccess import *

DATA_PATH = "DATA"
SAVED_FILE = "SchedTopo.txt"

DAY_MAX_TIME = 1439
DAY_BEGIN_TIME = 240

MAX_RANGE = 100000

PER_SATELLITE_LIMIT_ALL = 6

PER_SATELLITE_LIMIT_MEO = 2
PER_SATELLITE_LIMIT_GROUND = 1
PER_SATELLITE_LIMIT_LEO = 1
PER_SATELLITE_LIMIT_GEO = 1



class SatelliteItem():
    def __init__(self,node1, node2, tstamps,distance):
        self.node1 = node1
        self.node2 = node2
        self.tstamps = int(tstamps)
        self.distance = float(distance)

        self.layer = self.node2[:2]

def CutSorted(clslist,cutpoint=None):
    cut_stamps = []
    s_i = []
    for i in range(len(clslist)-1):
        if clslist[i].tstamps != clslist[i+1].tstamps:
            cut_stamps.append(i+1)
    n = 0
    for num in cut_stamps:
        s_i.append(clslist[n:num])
        n = num
    s_i.append(clslist[cut_stamps[-1]:])

    if cutpoint:
        return cut_stamps
    else:
        return s_i


def SortedSelectedSLinks(fname):
    f = fname
    lines = f.readlines()
    satellite_items = []
    for line in lines:

        elem = line.split()
        s_item = SatelliteItem(elem[0],elem[1],elem[2],elem[3])
        satellite_items.append(s_item)
    satellite_sorted_items = sorted(satellite_items, key=attrgetter('tstamps','layer','distance')) # sort by tstamps

    OriginalTopoStamps = CutSorted(satellite_sorted_items)

    TopoSts = TopoStamps(OriginalTopoStamps)

    return TopoSts


def TopoStamps(Original_topo_stamps):
    TopoStamps = []
    for original_topo_stamp in Original_topo_stamps:
        TopoStamp = []

        temp_g = []
        temp_m = []
        temp_l = []
        for item in original_topo_stamp:
            m_orbit = []
            if item.layer == "GE" :
                temp_g.append(item)
            if item.layer == "LE" :
                temp_l.append(item)
            if item.layer == "ME" :
                temp_m.append(item)

        #temp_m
        temp = []
        for i in range(len(temp_m)-1):
            if temp_m[i].node2[:-1] != temp_m[i-1].node2[:-1]:
                temp.append(temp_m[i])
        temp_m = temp[:]

        TopoStamp.append(temp_g[PER_SATELLITE_LIMIT_GEO-1])
        TopoStamp.append(temp_l[PER_SATELLITE_LIMIT_LEO-1])

        for i in range(PER_SATELLITE_LIMIT_MEO):
            TopoStamp.append(temp_m[i])        #BUG!!!!!

        TopoStamps.append(TopoStamp)
    return TopoStamps


#def SatelliteTopoDesign(ClsSortedList):
#   def HandleSLinks(SatelliteOrignalLinks):
#     SingleItems = []
#     for SingleSatelliteOrignalLinks in SatelliteOrignalLinks:
#         for SingleSchedSLinks in SingleSatelliteOrignalLinks:
#             SingleItems.append(SingleSchedSLinks)
#     return SingleItems
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
            T = SortedSelectedSLinks(f)
            f.close()
            print(T)