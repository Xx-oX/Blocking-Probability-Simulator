import Model
import pandas as pd

BPTable = []
EVTable = []
EventTable = []
record = False


def subSim(s, q):
    l = 0.01
    t = 0.01 / l
    BPList = []
    EVList = []
    if record:
        TimeUnitTable = []
        ArrivalTable = []
        DeparturnTable = []
        BlockedTable = []
    while l <= 10:
        m = 0.01
        while m <= 10.24:
            EVList.append(l / m)
            totalBP = 0.0
            for i in range(10):
                model = Model.Model(s, q, l, m, t)
                for j in range(100000):
                #for j in range(100):
                    model.update()
                    if model.arrival():
                        model.come()

                    if record:
                        TimeUnitTable.append(t*j)
                        ArrivalTable.append(model.nArrival)
                        DeparturnTable.append(model.nDparture)
                        BlockedTable.append(model.nBlock)

                if model.nArrival != 0:
                    totalBP += model.nBlock / model.nArrival

            BPList.append(totalBP / 10)
            m *= 4
        l *= 10

    BPTable.append(BPList)
    EVTable.append(EVList)
    if record:
        EventTable.append([TimeUnitTable, ArrivalTable, DeparturnTable, BlockedTable])


def simulate(index):
    if index == 0:
        subSim(1, 0)
    elif index == 1:
        subSim(1, 1)
    elif index == 2:
        subSim(5, 0)
    elif index == 3:
        subSim(5, 5)
    elif index == 4:
        subSim(10, 0)
    elif index == 5:
        subSim(10, 10)


def output(i, mode, a_fromCsv=False, a_print=False, a_toCsv=False):
    BPTable.clear()
    if record:
        EventTable.clear()

    if mode == 'BPTable':
        if a_fromCsv:
            df = pd.read_csv('BlockingProb' + str(i) + '.csv')
        else:
            simulate(i)
            dic = {'Erlang value': EVTable[0], 'Blocking Prob.': BPTable[0]}
            df = pd.DataFrame(dic)
        if a_toCsv:
            df.to_csv('BlockingProb' + str(i) + '.csv')
        if a_print:
            print(df)
        return df
    elif mode == 'EventTable' and record:
        if a_fromCsv:
            df = pd.read_csv('Event' + str(i) + '.csv')
        else:
            simulate(i)
            dic = {'Time unit': EventTable[0][0], 'Arrivals': EventTable[0][1], 'Departures': EventTable[0][2], 'Blocked': EventTable[0][3]}
            df = pd.DataFrame(dic)
        if a_toCsv:
            df.to_csv('Event' + str(i) + '.csv')
        if a_print:
            print(df)
        return df
    else:
        return pd.DataFrame({})

def test(s, q, l, m, t):
    totalBP = 0.0
    for i in range(10):
        model = Model.Model(s, q, l, m, t)
        for j in range(100000):
            # for j in range(100):
            model.update()
            if model.arrival():
                model.come()

        if model.nArrival != 0:
            totalBP += model.nBlock / model.nArrival
    print('Blocking Probability: ', totalBP / 10)
    #print('arrival:', model.nArrival, ', block:', model.nBlock, ' ,departure:', model.nDparture)