import os
from datetime import datetime

#DATA_PATH = "/Users/likexin/PycharmProjects/HandleAccess/src/Data"
DATA_PATH = "../Data"

SAVED_FILE = "SchedTopo.txt"


# transfer UTCG format to sec format such as : "04:00:00" to "14400"
def HandleDateTime(UTCG):
    str = UTCG.split(':')
    sec = (int(str[0]))*3600 + (int(str[1]))*60 + (int(str[2]))
    return sec



# handle A LINE written like
# "2  (StartTime)23 Mar 2018 05:20:36.864  (StopTime)23 Mar 2018 06:28:39.820  (Duration)4082.956"
#
# to a str like "StartTime StopTime"
#
# return "StartTime StopTime"
def line_split(line):
    start_time_str = line[40:48]
    stop_time_str = line[68:76]
    Duration = line[89:94]
    StartTime = HandleDateTime(start_time_str)
    StopTime = HandleDateTime(stop_time_str)
    s_tr = str(StartTime) + ' ' + str(StopTime)
    return s_tr
    # start_flag = True if (datetime.strptime(TIME_START, "%d %b %Y %H:%M:%S") - \
        #     datetime.strptime(start_time_str, "%d %b %Y %H:%M:%S")).total_seconds() >= 0 else False
        # stop_flag = True if (datetime.strptime(TIME_STOP, "%d %b %Y %H:%M:%S") - \
        #                      datetime.strptime(stop_time_str, "%d %b %Y %H:%M:%S")).total_seconds() <= 0 else False
        # if start_flag and stop_flag:
        #     MATRIX[INDEX_MAP[star_a], INDEX_MAP[star_b]] = 1
        #     MATRIX[INDEX_MAP[star_b], INDEX_MAP[star_a]] = 1
        # else:
        #     continue



# handle a pair of MEO11-to-LEO11 access
#
# return "MEO11 LEO11 StartTime StopTime"
def handle_records(node1, node2, records):
    command = []
    for record in records:
        s__tr = line_split(record)
        S__tr = node1 +' ' + node2 +' ' + s__tr
        command.append(S__tr)
        values = S__tr.split(" ")
        addLink = "py net.addLink(%s, %s, sch_time=%s)" % (node1, node2, values[2])
        print(addLink)
        delLinkBetween = "py net.delLinkBetween(%s, %s, sch_time=%s)" % (node1, node2, values[-1])
        print(delLinkBetween)

    #print(command)
    return command


def output_str(lists):
    for list in lists:
        print(list)


# output
# def output_matrix():
#     global MATRIX
#     f = open("SAVED_MATRIX_FILE", "w")
#     for i in range(STAR_COUNT):
#         for j in range(STAR_COUNT):
#             f.write(str(MATRIX[i][j]) + ", ")
#         f.write("\n")
#     f.close()


# read a file "XXX.txt" and split data, return "records" ,as a directory, that contained all link changes of node"XXX"
def handle(f):
    line = f.readline()
    commands = []
    while line:
        if line.startswith("MEO") or line.startswith("LEO") or line.startswith("GEO"):

            # find 2 nodes of link
            nodes = line.split('-')
            node1 = nodes[0]
            node2 = nodes[-1].strip()

            f.readline()
            f.readline()
            f.readline()

            records = []
            line = f.readline()
            while len(line) > 2:
                records.append(line)
                line = f.readline()
            command = handle_records(node1, node2, records)
            commands = command[:]
        else :
            if not line:
                break
            line = f.readline()
    #output_str(commands)
    return commands




def get_access_pairs():
    pair_files = os.listdir(DATA_PATH)
    os.chdir(DATA_PATH)
    AllCmds = []
    for pair_file in pair_files:
        f = open(pair_file, "r")
        cmd = handle(f)
        AllCmds.append(cmd)
        f.close()
    os.chdir("..")
    #output_str()
    # output()



if __name__ == '__main__':
    get_access_pairs()
