from operator import itemgetter, attrgetter
import sys
import os
from datetime import datetime


DATA_PATH = "DATA"
SAVED_FILE = "SelectedSources.txt"


#Tansfrom from "04:00:00" to "240"
def TimeStamps(TimeStr):
    if TimeStr.find(':')==2:
        Timestr = TimeStr.split(':')
        Timestamps = int(Timestr[0])*3600 + int(Timestr[1])*60 + int(Timestr[2])
        Ts = int(Timestamps/60)
        return str(Ts)
    else:
        pass

def LineSplit(line):
    t = line[30:38]
    r = line[82:90]
    Tstamps = TimeStamps(t)
    return Tstamps, r


def SingleLine(nodes, Linesplit):
    return list(nodes) + list(LineSplit(Linesplit))


def HandleSources(llines):
    SourceLines = llines

    # clear data
    SelectedSources = []
    for Source in SourceLines:
        if Source.startswith("MEO") or Source.startswith("                  "):
            if Source.find("Time") < 0 and Source.find('--') < 0:
                SelectedSources.append(Source)
    return SelectedSources


def HandleSelectedSources(selected_sources):
    nodeslines = []
    FormLines = []
    for edSource in selected_sources:
        if edSource.startswith("MEO") or edSource.startswith("GEO") or edSource.startswith("LEO"):
            n = edSource.strip()
            nodeslines.append(n.split("-To-"))
        elif edSource.startswith("                  "):
            FormLines.append(SingleLine(nodeslines[-1], edSource))
        else:
            continue
    return FormLines



#Open DATA_PATH and save files
def get_access_pairs():
    pair_files = os.listdir(DATA_PATH)
    os.chdir(DATA_PATH)
    source = []


    for pair_file in pair_files:
        if pair_file.endswith("txt"):
            f = open(pair_file, "r")
            SourceLines = f.readlines()
            SingleSatelliteLinks = HandleSources(SourceLines)
            f.close()

            FormLines = HandleSelectedSources(SingleSatelliteLinks)
            Form = sorted(FormLines, key=itemgetter(2, 1, 3))
            source.append(Form)


            # for s in source:
            #     print(s)

            #write
            with open(SAVED_FILE, 'a+') as f:
                for s in Form:
                    sStr = ""
                    for i in s:
                        sStr = sStr + "%s "%i
                    f.write(sStr)
                    f.write('\n')


    os.chdir("..")


    return source







if __name__ == '__main__':

    sitem = get_access_pairs()
    for s in sitem:
        print(s)

