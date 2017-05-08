
# coding: utf-8

# In[11]:

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
conservativerate = 0.001
numberofsentences = 200000
threshold = .001

#language = "611" #English
language = "584" #French
#language = "2253" #German
#language = "3856" #Japanese

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



