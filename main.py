import re
from collection import defaultdict
from copy import deepcopy


class KB():
    def __init__():
        self.kb = []
        # deduce[q] is the list of atoms that q can help to deduce
        # depend[q] is the list of atoms that q depends on to deduce
        self.deduce = {"null" = []}
        self.depend = {}
        return

    def addToKBFromFile(self, fileName):
        f = open(fileName, "r")
        for line in f:
            tmp = line.replace("]", "").split("[")
            for i in range(len(tmp)):
                tmp[i] = tmp[i].rstrip().split()
            del tmp[0]
            self.addToKB(tmp)
        self.kb = sorted(self.kb, key=lambda item: len(item[2]))
        self.kb = sorted(self.kb, key=lambda item: len(item[1]))
        self.kb = sorted(self.kb, key=lambda item: len(item[0]))
        f.close()
        return

    def addToKB(self, item):
        self.kb.append(tmp)
        q = tmp[0]
        pPositive = tmp[1]
        # pNegative = tmp[2]
        if len(pPositive) + len(pPositive) == 0:
            self.deduce["null"].append(q)
            self.depend[q] = []
        for item in pPositive:
            self.deduce[item].append(q)
            self.depend[q].append(item)
        return

    def calculateConclusions(self):
        c = []
        queue = []
        deduce = deepcopy(self.deduce)
        depend = deepcopy(self.depend)

        for item in deduce["null"]:
            queue.append(item)

        while len(queue) != 0:
            q = queue[0]
            del queue[0]

            if self.depend[q] == []:
                c.append(q)
                for item in deduce[q]:
                    if q in depend[item]:
                        depend[item].remove(q)
                    queue.append(item)
        return c
