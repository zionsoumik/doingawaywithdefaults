
# coding: utf-8

# In[ ]:

class Sentence(object):
    def __init__ (self, infoList):
        self.language = infoList[0]
        self.inflection = infoList[1]
        self.sentenceStr = infoList [2]
        self.sentenceList = infoList[2].split()
        
    def indexString(self,key):
        for word in self.sentenceList:
            if key in word:
                return self.sentenceList.index(word)
        
        

