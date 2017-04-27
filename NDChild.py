
# coding: utf-8

# In[ ]:

class NDChild(object):
    def __init__ (self, learningrate, conslearningrate):
        
        self.grammar = {"SP": .5, "HIP": .5, "HCP": .5, "OPT": .5, "NS": .5, "NT": .5,"WHM": .5, "PI": .5, "TM": .5, "VtoI": .5, "ItoC": .5,"AH": .5, "QInv": .5}
        self.r = learningrate #simulation will pass child a learning rate
        self.conservativerate = conslearningrate
    
    def consumeSentence(self, s): #child is fed a list containing [lang, inflec, sentencestring]
        self.findEtrigger("SP", s)    #parameter 1
        self.findEtrigger("HIP", s)   #parameter 2
        self.findEtrigger("HCP", s)   #parameter 3
        #self.findEtrigger("OPT", s)  #parameter 4
        #self.findEtrigger("NS", s)   #parameter 5
        #self.findEtrigger("NT", s)   #parameter 6
        self.findEtrigger("WHM", s)   #parameter 7
        self.findEtrigger("PI", s)   #parameter 8
        self.findEtrigger("TM", s)    #parameter 9
        #self.findEtrigger("VtoI", s) #parameter 10
        #self.findEtrigger("ItoC", s) #parameter 11
        self.findEtrigger("AH", s)    #parameter 12
        #self.findEtrigger("QInv", s) #parameter 13
      
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
            
         
        elif parameter is "HCP": #third parameter Head in CP
            if s.inflection == "Q":
                if s.sentenceList[-1] == 'ka' or ("ka" not in s.sentenceList and s.sentenceList[-1] == "Aux"): #ka or aux last in question
                    self.adjustweight("HCP", 1, self.r)
                
                elif s.sentenceList[0] == "ka" or ("ka" not in s.sentenceList and s.sentenceList[0]=="Aux"): #ka or aux first in question
                    self.adjustweight("HCP", 0, self.r)
        
        elif parameter is "AH": 
            if (s.inflection == "DEC" or s.inflection == "Q") and ("Aux" not in s.sentenceStr and "Never" in s.sentenceStr and "Verb" in s.sentenceStr and "O1" in s.sentenceStr):
                neverPos = s.indexString("Never")
                verbPos = s.indexString("Verb")
                O1Pos = s.indexString("O1")
            
                if (neverPos > -1 and verbPos == neverPos+1 and O1Pos == verbPos+1) or (O1Pos > -1 and verbPos == O1Pos+1 and neverPos == verbPos + 1):
                    self.adjustweight("AH", 1, self.r)
                    
            ####NEED TO THINK ABOuT CODE TOWARDS 0
        
        elif parameter is "WHM":
            if s.inflection == "Q" and "+WH" in s.sentenceStr:
                if ("+WH" in s.sentenceList[0]) or ("P" == s.sentenceList[0] and "O3[+WH]" == s.sentenceList[1]):
                    self.adjustweight("WHM",1,self.conservativerate)
                else:
                    self.adjustweight("WHM",0,self.r)
        
        elif parameter is "PI":
            if "P" in s.sentenceList and "O3" in s.sentenceList:
                if abs(s.indexString("P") - s.indexString("O3")) > 1:
                    self.adjustweight("PI", 1, self.r)
                
                elif s.inflection == "Q" and ((s.indexString("P") + s.indexString("O3")) == 1):
                    self.adjustweight ("PI",0,self.r)
                    
        
        
        elif parameter is "TM":
            if "[+WA]" in s.sentenceStr:
                self.adjustweight("TM",1,self.r)
            elif "O1" in s.sentenceList and "O2" in s.sentenceList and (abs(s.sentenceList.index("O1")-s.sentenceList.index("O2")) > 1):
                self.adjustweight("TM",0,self.r)
                
        elif parameter is "ItoC":
            sp = self.grammar['SP']
            hip = self.grammar['HIP']
            hcp = self.grammar['HCP']

            if sp < 0.5 and hip < 0.5: # (Word orders 1, 5)
                Sindex = s.sentenceList.index("S")
                if (Sindex > 0 and s.inflection == "DEC") and s.sentenceList.index("Aux") == Sindex + 1:
                    self.adjustweight("ItoC", 0, self.r)

            elif sp > 0.5 and hip > 0.5: # (Word orders 2, 6)
                if (s.inflection == "DEC"):
                    AuxIndex = s.sentenceList.index("Aux")
                    if (AuxIndex > 0 and s.sentenceList.index("S") == AuxIndex + 1):
                        self.adjustweight("ItoC", 0, self.r)

            elif sp > 0.5 and hip < 0.5 and hcp > 0.5 and s.inflection == "DEC":
                if s.sentenceList.index("Verb") == s.sentenceList.index("Aux") + 1:
                    self.adjustweight("ItoC", 0, self.r)

            elif sp < 0.5 and hip > 0.5 and hcp < 0.5 and s.inflection == "DEC":
                if s.sentenceList.index("Aux") == s.sentenceList.index("Verb") + 1:
                    self.adjustweight("ItoC", 0, self.r)

            elif sp > 0.5 and hip < 0.5 and hcp < 0.5 and ('ka' in s.sentenceList):
                if s.inflection == "DEC" and "Aux" not in s.sentence:
                    if (s.sentenceList.index("Verb") == s.sentenceList.index("Never") + 1):
                        self.adjustweight("ItoC", 0, self.r)

            elif sp < 0.5 and hip > 0.5 and hcp > 0.5 and ('ka' in s.sentenceList):
                if s.inflection == "DEC" and "Aux" not in s.sentence:
                    if s.sentenceList.index("Never") == s.sentenceList.index("Verb") + 1:
                        self.adjustweight("ItoC", 0, self.r)
                
                    
                
         
                        
        else:
            raise ValueError("This parameter isn't implemented yet")
    
    
    def adjustweight(self, parameter, direction, rate):
        if direction == 0:
            self.grammar[parameter] -= rate*self.grammar[parameter]
        elif direction == 1:
            self.grammar[parameter] += rate*(1-self.grammar[parameter])
            

