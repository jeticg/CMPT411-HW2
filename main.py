import re
from collections import defaultdict
from copy import deepcopy


class KB():
    def __init__(self):
        self.kb = []
        # deduce[q] is the list of sentence index that q can help to deduce
        # depend[q] is the list of sentence index deduces q
        # fail[q] is the list of sentence index that fails if q
        self.deduce = {"null": []}
        self.depend = {}
        self.fail = {}
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

    def addToKB(self, sentence):
        index = len(self.kb)
        self.kb.append(sentence)
        q = sentence[0]
        pPositive = sentence[1]
        pNegative = sentence[2]

        if len(pPositive) + len(pPositive) == 0:
            self.deduce["null"].append(index)

        self.depend[q].append(index)

        for item in pPositive:
            self.deduce[item].append(index)
        for item in pNegative:
            self.fail[item].append(index)
        return

    def calculateConclusions(self):
        deduce = deepcopy(self.deduce)
        depend = deepcopy(self.depend)
        fail = deepcopy(self.fail)
        kb = deepcopy(self.kb)

        c = []
        queue = []

        def concludeQ(q, c=c, queue=queue, deduce=deduce, depend=depend, fail=fail, kb=kb):
            c.append(q)

            # remove q from atoms that depends on q
            for index in deduce[q]:
                kb[index][1].remove(q)
                if len(kb[index][1]) + len(kb[index][2]) == 0:
                    queue.append(index)

            # remove sentences that fails if q
            for index in fail[q]:
                kb[index][2] = ["null"]
                sub_q = kb[index][0]
                depend[sub_q].remove(index)
                # if sub_q cannot be derived from any other sentences, fail q
                if len(depend[sub_q]) == 0:
                    failQ(sub_q)

        def failQ(q, c=c, queue=queue, deduce=deduce, depend=depend, fail=fail, kb=kb):
            c.append("~" + q)
            # remove q from atoms that depends on ~q
            for index in fail[q]:
                kb[index][2].remove(q)
                if len(kb[index][1]) + len(kb[index][2]) == 0:
                    queue.append(index)

            # remove sentences that fails if ~q
            for index in deduce[q]:
                kb[index][2] = ["null"]
                sub_q = kb[index][0]
                depend[sub_q].remove(index)
                # if sub_q cannot be derived from any other sentences, fail q
                if len(depend[sub_q]) == 0:
                    failQ(sub_q)

        def judgeSentence(sentence, c=c, queue=queue, deduce=deduce, depend=depend, fail=fail, kb=kb):
            q = sentence[0]
            pPositive = sentence[1]
            pNegative = sentence[2]

            if len(pPositive) + len(pNegative) == 0:
                concludeQ(q)
            if pNegative == ["null"]:
                failQ(q)

        for index in deduce["null"]:
            queue.append(index)

        while len(queue) != 0:
            tmp = self.kb[queue[0]]
            judgeSentence(tmp)

        return c

if __name__ == '__main__':
    kb = KB()
    kb.addToKBFromFile("test1.txt")
    print kb.calculateConclusions()
