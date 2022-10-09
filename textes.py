import random
import re


class Textes:
    def __init__(self, age=0):
        self.greetings = ["Bonjour, Maître","Comment ça va ?","Encore une belle journée !"]
        self.byes = ["Aurevoir, Maître", "à plus, très cher", "A la revoyure !"]
        self.age = age

    def getFirstSentence(self):
        return random.choices(self.greetings)[0]

    def getLastSentence(self):
        return random.choices(self.byes)[0]

    def getWordsPositions(self,phrase):
        pos=[]
        words=phrase.split(" ")
        for word in words:
            #print("'"+word+"'")
            for match in re.finditer(word,phrase):
                minpos=match.start()/100
                maxpos=match.end()/100
                pos.append((round(1+minpos, 2), round(1+maxpos, 2)))
                break
        return pos

"""phrase="I WILL PROTECT YOU NOW!"
t=Textes()
pos=t.getWordsPositions(phrase)
#print("phrase: ",phrase)
#print(pos)


for (deb, fin) in pos:
    print("de "+str(deb)+" a "+str(fin))
    i = deb
    while i < fin:
        print(str(format(i, '.2f')))
        i += 0.01
        i = round(i, 2)"""

