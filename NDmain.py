from NDChild import NDChild
from time import clock
from random import choice
import csv
from datetime import datetime
import os
from sys import argv
from argparse import ArgumentParser
from Sentence import Sentence
import NDresults

#GLOBALS
rate = 0.02
conservativerate = 0.01
numberofsentences = 200000
threshold = .001

#language = "611" #English
#language = "584" #French
#language = "2253" #German
language = "3856" #Japanese

infoFile = open('EngFrJapGerm.txt','rU')

LD = []

def pickASentence(languageDomain):

    return choice(languageDomain)

def createLD():
    for line in infoFile:
        [grammStr, inflStr, sentenceStr] = line.split("\t")
        sentenceStr = sentenceStr.rstrip()
        s = Sentence([grammStr, inflStr, sentenceStr]) #constructor creates sentenceList
        if grammStr == language:
            LD.append(s)



####   MAIN
createLD()

ndr = NDresults.NDresults()

ndr.writeOutputHeader(611, 1, numberofsentences)

aChild = NDChild(rate, conservativerate)

for i in range(numberofsentences):
    s = pickASentence(LD)
    aChild.consumeSentence(s)
    ndr.checkIfParametersMeetThreshold(threshold, aChild.grammar, i)

writeResults(aChild.grammar, i)

print aChild.grammar

infoFile.close()
