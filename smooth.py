#Imports
import re
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt 
import math
import operator

#Regex
sentenceEnders = re.compile(r"""
    (?:(?<=[.!?])|(?<=[.!?]['"]))
    (?<!  Mr\.   )
    (?<!  Mrs\.  )
    (?<!  Jr\.   )
    (?<!  Dr\.   )
    (?<!  Prof\. )
    (?<!  Sr\.   )
    (?<!  Rs\.   )
    \s+
    """, re.I | re.VERBOSE)

#Empty Dictionaries
learningDict = {}
newLearningDict = {}

#Function which smooths the sentence
def turingSmoothing(fileName, learn, drawGraph):
    with open(fileName, 'r') as myFile:
        text = myFile.read().replace('\n', ' ')
    myList = []
    sentenceList = sentenceEnders.split(text)
    for s in sentenceList:
        myList.append(s.strip())
    for i in range(len(myList)):
         myList[i] = myList[i].replace('\r', '').strip()
    for b in range(1, 7):    
        allWords = []
        for line in myList:
            words = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", line)
            for word in zip(*[words[i:] for i in range(b)]):
                allWords.append(word)
        
        frequencyCount = Counter(allWords).most_common()
        onlyFrequency = []
        for i in frequencyCount:
            onlyFrequency.append(i[1])
        onlyFrequency.sort()
        freqOfFreq = [0 for i in range(onlyFrequency[-1] + 2)]
        for i in onlyFrequency[::-1]:
            if freqOfFreq[i] == 0:
                freqOfFreq[i] = onlyFrequency.count(i)
        freqOfFreq.sort()
        print onlyFrequency[-1]
        newFreq = freqOfFreq[::-1]
        for i in range(len(newFreq)):
            if newFreq[i] == 0:
                breakPoint = i
                break
        for i in range(breakPoint, len(newFreq)):
            newFreq[i] = newFreq[breakPoint - 1]*pow(0.92, i-breakPoint)
        finalFreq = {}
        for i in frequencyCount:
            r = i[1]
            finalFreq[i] = (1.0*(r+1)*newFreq[r+1])/newFreq[r]
        sortfinalFreq = list(reversed(sorted(finalFreq, key=operator.itemgetter(1))))
        x = []
        y = []
        for k in range(len(sortfinalFreq)):
            x.append(math.log(float(k + 1)))
            y.append(math.log(float(sortfinalFreq[k][1])))
        if learn == True:
            learningDict[fileName] = [b, [1, 2]]
        else:
            newLearningDict[fileName] = [b, [3, 4]]
        if drawGraph == True:
            plt.plot(x, y, 'k-')
            #plt.savefig(fileName + '_' + str(b) + '.png')
            #plt.close()
            plt.show()
            print "Plotting"

#Compare corpus and tell the author. Not fully implemented
def matchCorpus(fileName):
    newFile = open(fileName, 'r')
    turingSmoothing(fileName, False, False)
    flag = 0
    for i in learningDict.keys():
        for j in range(1, 7):
            print learningDict[i][j][0]
    for i in learningDict.keys():
        for a in range(1, 7):
            xCoordinates = learningDict[i][a][0]
            yCoordinates = learningDict[i][a][1]
            newXCoordinates = newLearningDict[fileName][a][0]
            newYCoordinates = newLearningDict[fileName][a][1]
            for k in range(min(len(xCoordinates), len(newXCoordinates))):
                xa = xCoordinates[k]
                xb = newXCoordinates[k]
                ya = yCoordinates[k]
                yb = newYCoordinates[k]
                dist = math.sqrt((xa-xb)^2 + (ya-yb)^2)
                if dist > 1:
                    flag = 1
                    break
            if flag != 1:
                print fileName, " is Similar to ", i, " for ", k, " grams"
                break

#Smoothing of all n-grams
for i in range(1, 6):
    turingSmoothing('corpus' + str(i) + '.txt', True, True)
matchCorpus('corpus6.txt')
