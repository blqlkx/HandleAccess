import xlrd, os

PATH = "Handle_delay"


def get_delay():
    files = os.listdir(PATH)
    os.chdir(PATH)
    for file in files:
        HandleFile(file)


class Data:
    def __init__(self, time, node1, h_distance, clock, node2):
        self.UCTG_Time = time
        self.node1 = node1
        self.delay = h_distance
        self.clock = clock
        self.node2 = node2


def HandleFile(f_name):

    f = xlrd.open_workbook(f_name + ".xlsx")

    sheets = f.sheets()
    for sheet in sheets:
        nrows = sheet.nrows
        _to_n_data = []
        rows = []
        cols = []
        nodes = sheet.row_values(0)
        for i in range(2, nrows):
            rows = sheet.row_values(i)
            rows = [1000000 if x == '' else x for x in rows]
            data = Data(time=i-2, node1=nodes[rows.index(min(rows))], h_distance=min(rows), node2=None, clock=None)
            # data.delay = min(rows)
            # node = rows.index(min(rows))
            # data.node = nodes[node]
            # data.UCTG_Time = i-2
            _to_n_data.append(data)

            """the result is like 
            '10029.5375 3 0     9876.277821 3 1     9723.092362 3 2     9570.026241 3 3     9417.126817 3 4
            """

        n_to_n_data = HandleData(_to_n_data, f_name)



def delay(num):
    """how to define delay
    """
    return float(num/86400)


def HandleData(_to_n_data, n2):
    n_to_n_data = []
    node2 = n2
    clocks = []
    for i in range(1, len(_to_n_data)):
        if _to_n_data[i].node1 != _to_n_data[i-1].node1:
            data = Data(h_distance=delay(_to_n_data[i].delay), node1=_to_n_data[i].node1, time=None, node2=node2, clock=i)
            n_to_n_data.append(data)
        else:
            continue
    for data in n_to_n_data:
        print(data.node1, data.node2, data.delay, data.clock)

    return n_to_n_data



if __name__ == '__main__':
    HandleFile("meo-122")
