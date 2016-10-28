import random


class KBTestCaseGenerator():
    def __init__(self, length=10, atoms=10):
        self.generate(length, atoms)
        return

    def generate(self, length, atoms):
        self.atomList = []
        self.sentenceList = []
        for i in range(atoms):
            self.atomList.append('a' + str(i))
        for i in range(length):
            sentence = [random.randint(0, atoms-1), [], []]
            for j in range(random.randint(0, atoms/2)):
                tmp = random.randint(0, atoms-1)
                if tmp != sentence[0] and tmp not in sentence[1]:
                    sentence[1].append(tmp)
            for j in range(random.randint(0, atoms/2)):
                tmp = random.randint(0, atoms-1)
                if tmp != sentence[0] and tmp not in sentence[2]:
                    sentence[2].append(tmp)
            self.sentenceList.append(sentence)
        return

    def writeToFile(self, fileName):
        f = open(fileName, "w")
        for sentence in self.sentenceList:
            f.write("[" + self.atomList[sentence[0]] + " [")
            for i in range(len(sentence[1])):
                if i != len(sentence[1])-1:
                    f.write(self.atomList[sentence[1][i]] + " ")
                else:
                    f.write(self.atomList[sentence[1][i]])
            f.write("] [")
            for i in range(len(sentence[2])):
                if i != len(sentence[2])-1:
                    f.write(self.atomList[sentence[2][i]] + " ")
                else:
                    f.write(self.atomList[sentence[2][i]])
            f.write("]]\n")
        f.close()
        return
if __name__ == '__main__':
    g = KBTestCaseGenerator()
    g.writeToFile("test3.txt")
