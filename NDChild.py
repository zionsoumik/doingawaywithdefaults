
# coding: utf-8

# In[ ]:

class NDChild(object):
    def __init__ (self, learningrate):
        
        self.grammar = {"SP": .5, "HIP": .5, "HCP": .5, "OPT": .5, "NS": .5, "NT": .5,"WHM": .5, "PI": .5, "TM": .5, "VtoI": .5, "ItoC": .5,"AH": .5, "QInv": .5}
        self.r = learningrate #simulation will pass child a learning rate
          
    
    def consumeSentence(self, s): #child is fed a list containing [lang, inflec, sentencestring]
        self.findEtrigger("SP", s)
        self.findEtrigger("HIP", s)
        self.findEtrigger("HCP", s)
        #self.findEtrigger("OPT", s)
        #self.findEtrigger("NS", s)
        #self.findEtrigger("NT", s)
        #self.findEtrigger("WHM", s)
        #self.findEtrigger("PI", s)
        #self.findEtrigger("TM", s)
        #self.findEtrigger("VtoI", s)
        #self.findEtrigger("ItoC", s)
        #self.findEtrigger("AH", s)
        #self.findEtrigger("QInv", s)
      
    #etriggers for parameters
    
    def findEtrigger(self, parameter, s):
        if parameter is "SP": #first parameter Subject Position
            if "O1" in s.sentenceList and "S" in s.sentenceList and s.inflection == "DEC": #Check if O1 and S are in the sentence and sent is declarative
                O1index = s.sentenceList.index("O1")
                if O1index > 0 and O1index < s.sentenceList.index("S"): # Make sure O1 is non-sentence-initial and before S
                    self.adjustweight ("SP",1, self.r) #set towards Subject final
                elif O1index > 0 and O1index > s.sentenceList.index("S"): #S occurs before 01
                     self.adjustweight("SP",0,self.r) #set towards Subject initial
        
        elif parameter is "HIP": #second parameter Head IP, VP, PP, etc
            if "O3" in s.sentenceList and "P" in s.sentenceList:
                O3index = s.sentenceList.index("O3")
                Pindex = s.sentenceList.index("P")
                if O3index > 0 and Pindex == O3index + 1: #O3 followed by P and not topicalized
                    self.adjustweight ("HIP", 1, self.r)
                elif O3index > 0 and Pindex == O3index - 1:
                    self.adjustweight ("HIP", 0, self.r)
       
            elif s.inflection == "IMP" and "O1" in s.sentenceList and "Verb" in s.sentenceList:  #If imperative, make sure Verb directly follows O1
                if s.sentenceList.index("O1") == s.sentenceList.index("Verb") - 1:
                    self.adjustweight ("HIP", 1, self.r)
                elif s.sentenceList.index("Verb") == (s.sentenceList.index("O1") - 1):
                    self.adjustweight("HIP", 0, self.r)
            
            #elif "O3" in s.sentenceList and "P" in s.sentenceList: #P followed by O3 and not topicalized
             #   print s.sentenceList
            #  Pindex = s.sentenceList.index("P")
                #if Pindex > 0 and s.sentenceList.index("O3") == Pindex + 1:
                #    self.adjustweight("HIP", 0, self.r)
            #    O3index = s.sentneceList.index("O3")
            #   if O3index < Pindex:
            #       self.adjustweight("HIP", 0, self.r)
            
            #elif s.inflection == "IMP" and "O1" in s.sentenceList and "Verb" in s.sentenceList: #imperative and O1 follows V
            #    if s.sentenceList.index("Verb") == (s.sentenceList.index("O1") - 1):
            #        self.adjustweight("HIP", 0, self.r)
                      
            
        elif parameter is "HCP": #third parameter Head in CP
            if s.inflection == "Q":
                if s.sentenceList[-1] == 'ka' or ("ka" not in s.sentenceList and s.sentenceList[-1] == "Aux"): #ka or aux last in question
                    self.adjustweight("HCP", 1, self.r)
                
                elif s.sentenceList[0] == "ka" or ("ka" not in s.sentenceList and s.sentenceList[0]=="Aux"): #ka or aux first in question
                    self.adjustweight("HCP", 0, self.r)
                    
                        
        else:
            raise ValueError("This parameter isn't implemented yet")
    
    
    def adjustweight(self, parameter, direction, rate):
        if direction == 0:
            self.grammar[parameter] -= rate*self.grammar[parameter]
        elif direction == 1:
            self.grammar[parameter] += rate*(1-self.grammar[parameter])
            

