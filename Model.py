import random
import math


class Model():
    def __init__(self, a_server, a_queue, a_lamb, a_miu, a_t):
        #constructor
        self.nServer = a_server
        self.nQueue = a_queue
        self.lamb = a_lamb
        self.miu = a_miu
        self.delta = a_t
        self.nArrival = 0
        self.nBlock = 0
        self.nDparture = 0
        self.q = []
        self.s = []
        self.setup()

    def setup(self):
        for i in range(self.nQueue):
            self.q.append(0)
        for i in range(self.nServer):
            self.s.append(0)

    def arrival(self):
        return random.random() < (1 - math.exp(- self.lamb * self.delta))

    def departure(self):
        return random.random() < (1 - math.exp(- self.miu * self.delta))

    def come(self):
        self.nArrival += 1
        if self.nQueue == 0:
            indexS = self.detect(self.s, 0)
            if len(indexS) == 0:
                self.nBlock += 1
            else:
                self.s[indexS[0]] = 1
        else:
            for i in range(self.nQueue):
                if self.q[i] == 0:
                    self.q[i] = 1
                    return
            self.nBlock += 1

    def update(self):
        for i in range(self.nServer):
            if self.s[i] == 1:
                if self.departure():
                    self.s[i] = 0
                    self.nDparture += 1

        if self.nQueue != 0:
            indexQ = self.detect(self.q, 1)
            indexS = self.detect(self.s, 0)
            lQ = len(indexQ)
            lS = len(indexS)
            iQ = lQ-1
            if lS > 0:
                if lQ > 0:
                    for i in range(self.nServer):
                        if self.s[i] == 0 and iQ >= 0:
                            self.s[i] = self.q[indexQ[iQ]]
                            self.q[indexQ[iQ]] = 0
                            iQ -= 1

    def detect(self, list, n):
        #n = 0 or 1
        res = []
        for i in range(len(list)):
            if list[i] == n:
                res.append(i)
        return res

