import re
import sys
from collections import defaultdict
from copy import deepcopy


class KB():
    debug = False
    message = True

    def __init__(self):
        self.kb = []
        # deduce[q] is the list of sentence index that q can help to deduce
        # depend[q] is the list of sentence index deduces q
        # fail[q] is the list of sentence index that fails if q
        self.deduce = defaultdict(list)
        self.depend = defaultdict(list)
        self.fail = defaultdict(list)
        return

    def addToKBFromFile(self, fileName):
        f = open(fileName, "r")
        for line in f:
            tmp = line.replace("]", "").split("[")
            for i in range(len(tmp)):
                tmp[i] = tmp[i].rstrip().split()
            del tmp[0]
            tmp[0] = tmp[0][0]
            self.addToKB(tmp)
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
            if self.message:
                print "CORE [INFO]: conclude '" + q + "'"
            c.append(q)

            # remove q from atoms that depends on q
            for index in deduce[q]:
                if self.debug:
                    sys.stderr.write("CORE [DEBUG]: removing '" + q + "' from " + str(kb[index]) + "\n")
                kb[index][1].remove(q)
                if len(kb[index][1]) + len(kb[index][2]) == 0:
                    queue.append(index)

            # remove sentences that fails if q
            for index in fail[q]:
                for item in kb[index][2]:
                    if item != q:
                        fail[item].remove(index)
                kb[index][2] = ["null"]
                sub_q = kb[index][0]
                if self.debug:
                    sys.stderr.write("CORE [DEBUG]: removing sentence " + str(kb[index]) + " from depend['" + sub_q + "']\n")
                depend[sub_q].remove(index)
                # if sub_q cannot be derived from any other sentences, fail q
                if len(depend[sub_q]) == 0:
                    failQ(sub_q)

        def failQ(q, c=c, queue=queue, deduce=deduce, depend=depend, fail=fail, kb=kb):
            if self.message:
                print "CORE [INFO]: fail '" + q + "'"
            c.append("~" + q)
            # remove q from atoms that depends on ~q
            for index in fail[q]:
                if self.debug:
                    sys.stderr.write("CORE [DEBUG]: removing '" + q + "' from " + str(kb[index]) + "\n")
                kb[index][2].remove(q)
                if len(kb[index][1]) + len(kb[index][2]) == 0:
                    queue.append(index)

            # remove sentences that fails if ~q
            for index in deduce[q]:
                for item in kb[index][1]:
                    if item != q:
                        deduce[item].remove(index)
                kb[index][1] = ["null"]
                sub_q = kb[index][0]
                if self.debug:
                    sys.stderr.write("CORE [DEBUG]: removing sentence " + str(kb[index]) + " from depend['" + sub_q + "']\n")
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

        if self.debug:
            sys.stderr.write("CORE [DEBUG]: Beginning Initialisaion\n")

        for index in deduce["null"]:
            if self.debug:
                sys.stderr.write("CORE [DEBUG]: adding " + str(kb[index]) + " to queue\n")
            queue.append(index)

        if self.debug:
            sys.stderr.write("CORE [DEBUG]: Initialisaion Complete\n")

        if self.message:
            print "CORE [INFO]: Phase 1, workout all possible truth without fitting operators"

        while len(queue) != 0:
            tmp = kb[queue[0]]
            del queue[0]
            if self.debug:
                sys.stderr.write("CORE [DEBUG]: Processing " + str(tmp) + "\n")
            judgeSentence(tmp)

        if self.message:
            print "CORE [INFO]: Phase 2, fit operators to all atoms without dependency"

        for item in set(deduce.keys() + fail.keys()):
            if item not in depend and item != "null" and "~" + item not in c:
                if self.debug:
                    sys.stderr.write("CORE [DEBUG]: Nothing deduces '" + item + "', failing\n")
                failQ(item)

        if self.message:
            print "CORE [INFO]: Phase 3, work out the rest"

        while len(queue) != 0:
            tmp = kb[queue[0]]
            del queue[0]
            if self.debug:
                sys.stderr.write("CORE [DEBUG]: Processing " + str(tmp) + "\n")
            judgeSentence(tmp)

        return c

if __name__ == '__main__':
    kb = KB()
    for i in range(1, len(sys.argv)):
        kb.addToKBFromFile(sys.argv[i])
    print kb.calculateConclusions()
