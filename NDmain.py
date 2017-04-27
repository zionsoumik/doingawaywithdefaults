
# coding: utf-8

# In[1]:

from NDChild import NDChild
from time import clock
from random import choice
import csv
from datetime import datetime
import os
from sys import argv
from argparse import ArgumentParser
from Sentence import Sentence

#GLOBALS
rate = 0.02
conservativerate = .005
numberofsentences = 200
language = "611"

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

aChild = NDChild(rate, conservativerate)

for i in range(numberofsentences):
    s = pickASentence(LD)
    aChild.consumeSentence(s)
    

print aChild.grammar

        

infoFile.close()



# In[ ]:




# In[ ]:



