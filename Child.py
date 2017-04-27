class Child(object):
    def __init__(self):
        #This boolean is False unless the function checkIfLearned sets it to True (which happens when the grammar is acquired). The main program will while-loop until
        self.grammarLearned = False

        self.infoList = []
        
        #in time sits the number of sentences (discrete time units) the echild has been exposed to at the current time
        self.sentenceCount = 0

        self.grammar = [0,0,0,0,0,0,1,0,0,0,1,0,1]

        #Used to determine if a new grammar is being read in.
        #If so, expectedGrammar and currentGrammarID are updated accordingly
        self.currentGrammarID = '0'

        self.totalTime = 0

        self.oldGrammar = [-1] * 13
        
        self.timeCourseVector = [[-1,i] for i in range(0,13)]


    #Returns the index of value in the list, in this case it can find the value as a substring in the index of the list    
    def findIndex(self, value):
        return next((i for i, string in enumerate(self.infoList[3]) if value in string),-1)    


    '''
    Checks whether an eChild's parameter values
    have changed since the new sentence was processed.
    If any have changed, they are updated in old grammar
    and the timeCourseVector list's tuple corresponding
    to the parameter is updated with 'count' to reflect
    how many sentences have passed when the parameter
    was changed
    '''
    def haveParametersChanged(self):
        for i in range (0,13):
            if self.oldGrammar[i] != self.grammar[i]:
                self.timeCourseVector[i][0] = self.sentenceCount
                self.oldGrammar[i] = self.grammar[i]


    '''
    This function will set the current information about the sentence and the sentence itself for the child
    Runs everytime eChild is processing a new input sentence
    Infolist[0] contains target grammar
    Infolist[1] contains illoc
    Infolist[2] contains sentences
    '''
    def consumeSentence(self, info):
        get_bin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n)

        info = info.replace('\n','')
        info = info.replace('\"','')
        self.infoList =  info.rsplit("\t",3)
        self.infoList.append(list(self.infoList[2].split()))
        if self.currentGrammarID != self.infoList[0]:
            self.expectedGrammar = " ".join(get_bin(int(self.infoList[0]),13)).split()
            self.currentGrammarID = self.infoList[0]
    

    def isQuestion(self):
        return self.infoList[1] == "Q"
    

    def isImperative(self):
        return self.infoList[1] == "IMP"
    

    def isDeclarative(self):
        return self.infoList[1] == "DEC"  
    
    
    #Running current sentence through regex filters and other stuff
    def setParameters(self):
        
        if self.grammar[0] == 0:
            self.setSubjPos();   # Parameter 1
        
        if self.grammar[1] == 0:
            self.setHead()       # Parameter 2

        if self.grammar[2] == 0:
            self.setHeadCP()     # Parameter 3
            
        if not (self.grammar[3] == 0 and self.grammar[5] == 1):
            self.setObligTopic() # Parameter 4 - Obligatory Topic : Problem parameter

        if self.grammar[4] == 0:
            self.setNullSubj()   # Parameter 5

        if self.grammar[5] == 0:
            self.setNullTopic()  # Parameter 6

        if self.grammar[6] == 1:
            self.setWHMovement() # Parameter 7

        if self.grammar[7] == 0:
            self.setPrepStrand() # Parameter 8

        if self.grammar[8] == 0:
            self.setTopicMark()  # Parameter 9

        if self.grammar[9] == 0:
            self.vToI()          # Parameter 10

        if self.grammar[10] == 1:
            self.iToC()          # Parameter 11 - I to C movement : Problem parameter

        if self.grammar[11] == 0:
            self.affixHop()      # Parameter 12


        if self.grammar[12] == 1:
            self.questionInver() # Parameter 13 - Question Inversion : Problem parameter
        
        if(self.grammar == self.expectedGrammar):
            self.grammarLearned = True

        self.haveParametersChanged()

               
    #1st parameter
    def setSubjPos(self):
        if "O1" in self.infoList[2] and "S" in self.infoList[2]: #Check if O1 and S are in the sentence
            index = self.findIndex("O1") #Find index of O1
            if index > 0 and index < self.findIndex("S"): # Make sure O1 is non-sentence-initial and before S
                self.grammar[0] = 1

                
    #set to 0 if the regex is met
    #try to set subject position to 0
    def noSubjPos(self):
        if "O1" in self.infoList[2] and "S" in self.infoList[2]: #Check if O1 and S are in the sentence
            index = self.findIndex("S") #Find index of O1
            if index >= 0 and index < self.findIndex("O1"): # Make sure O1 is non-sentence-initial and before S
                self.grammar[0] = 0

    
    #2nd parameter
    def setHead(self):
        if "O3" in self.infoList[2] and "P" in self.infoList[2]:
            index = self.findIndex("O3")
            if index > 0 and self.findIndex("P") == index + 1: #O3 followed by P
                self.grammar[1] = 1
        #If imperative, make sure Verb directly follows O1
        elif self.isImperative() and "O1" in self.infoList[2] and "Verb" in self.infoList[2]:
            if self.findIndex("O1") == self.findIndex("Verb") - 1:
                self.grammar[1] = 1

    
    def noHead(self):
        if "O3" in self.infoList[2] and "P" in self.infoList[2]:
            index = self.findIndex("P")
            # If P followed by O3
            if index > 0 and self.findIndex("O3") == index + 1:
                self.grammar[1] = 0
        # If imperative, make sure Verb is directly followed by O1
        if self.isImperative() and "O1" in self.infoList[2] and "Verb" in self.infoList[2]:
            if self.findIndex("Verb") == self.findIndex("O1") - 1:
                self.grammar[1] = 1    

                
    #3rd parameter 
    def setHeadCP(self):
        if self.isQuestion():
            if self.infoList[3][-1] == 'ka' or ("ka" not in self.infoList[2] and self.infoList[3][-1] == "Aux"):
                self.grammar[2] = 1

    
    def noHeadCP(self):
        if self.isQuestion():
            if self.infoList[3][0] == "ka" or ("ka" not in self.infoList[2] and self.infoList[3][0] == "Aux"):
                self.grammar[2] = 0


    def containsTopicalizable(self):
        firstElement = self.infoList[3][0]
        return firstElement == 'S' or firstElement == 'O1' or firstElement == 'O2' or firstElement == 'O3' or firstElement == 'Adv'


    # 4th parameter
    def setObligTopic(self):
        if self.isDeclarative():
            if "O2" in self.infoList[2] and "O1" not in self.infoList[2] :
                self.grammar[5] = 1
                if self.grammar[3] == 1:
                    self.grammar[3] = 0
            else:
                if (self.containsTopicalizable()):
                    self.grammar[3] = 1


    # Out of obliqueness order
    def outOblique(self):
        i = self.findIndex("O1")
        j = self.findIndex("O2") 
        k = self.findIndex("P")
        l = self.findIndex("O3")

        if (i != -1 and i < j < k and l == k+1):  
            return False
        elif (l != -1 and l < j < i and k == l+1):
            return False
        elif (i != -1 and j != -1 and k != -1 and l != -1):
            return True

                
    #5th parameter
    #Only works for full, not necessarily with CHILDES distribution
    def setNullSubj(self):
        if self.isDeclarative() and 'S' not in self.infoList[2] and self.outOblique():
            self.grammar[4] = 1


    #6th parameter
    def setNullTopic(self):
        if 'O2' in self.infoList[2] and not 'O1' in self.infoList[2]:
            self.grammar[5] = 1

    
    #7th parameter
    def setWHMovement(self):
        if self.findIndex("+WH") > 0 and "O3[+WH]" not in self.infoList[2]:
            self.grammar[6] = 0

                
    #8th parameter
    def setPrepStrand(self):
        i = self.findIndex('P') #Get index of P
        j = self.findIndex('O3')#Get index of O3
        # If P and O3 are in the sentence, confirm they aren't adjacent
        if i != -1 and j != -1 and abs(i - j) != 1 :
                self.grammar[7] = 1
    
    
    #9th parameter
    def setTopicMark(self):
        if "WA" in self.infoList[2]: self.grammar[8] = 1 

    
    #10th parameter
    def vToI(self):
        i = self.findIndex("O1")
        j = self.findIndex("Verb")
        if i > 0 and j != -1 and abs(i - j) != 1 :
            self.grammar[9] = 1 

               
    def S_Aux(self):
        if self.isDeclarative():
            i = self.findIndex("S")
            return i > 0 and self.findIndex("Aux") == i + 1
        return False


    def Aux_S(self):
        if self.isDeclarative():
            i = self.findIndex("Aux")
            return i > 0 and self.findIndex("S") == i + 1
        return False


    def Aux_Verb(self):
        return self.isDeclarative() and (self.findIndex("Aux") == self.findIndex("Verb") - 1)


    def Verb_Aux(self):
        return self.isDeclarative() and (self.findIndex("Verb") == self.findIndex("Aux") - 1)


    def Never_Verb(self):
        return self.isDeclarative() and (self.findIndex("Never") == self.findIndex("Verb") - 1) and "Aux" not in self.infoList[2]

    
    def Verb_Never(self):
        return self.isDeclarative() and (self.findIndex("Verb") == self.findIndex("Never") - 1) and "Aux" not in self.infoList[2]


    def hasKa(self):
        return "ka" in self.infoList[2]


    #11th parameter
    def iToC(self):
        p1 = self.grammar[0]
        p2 = self.grammar[1]
        p3 = self.grammar[2]

        if p1 == 0 and p2 == 0 and p3 == 0 and self.S_Aux():
            self.grammar[10] = 0
        elif p1 == 1 and p2 == 1 and p3 == 1 and self.Aux_S():
            self.grammar[10] = 0
        elif p1 == 1 and p2 == 0 and p3 == 1 and self.Aux_Verb():
            self.grammar[10] = 0
        elif p1 == 0 and p2 == 1 and p3 == 0 and self.Verb_Aux():
            self.grammar[10] = 0
        elif p1 == 0 and p2 == 0 and p3 == 1 and self.S_Aux():
            self.grammar[10] = 0
        elif p1 == 1 and p2 == 1 and p3 == 0 and self.Aux_S():
            self.grammar[10] = 0
        elif p1 == 1 and p2 == 0 and p3 == 0 and (self.Never_Verb() or self.hasKa()):
            self.grammar[10] = 0
        elif p1 == 0 and p2 == 1 and p3 == 1 and (self.Verb_Never() or self.hasKa()):
            self.grammar[10] = 0
    

    def Verb_tensed(self):
        return (self.isDeclarative() or self.isQuestion()) and "Aux" not in self.infoList[2]


    #12th parameter                                          
    def affixHop(self):
        if self.Verb_tensed():
            i = self.findIndex('Never')
            j = self.findIndex('Verb')
            k = self.findIndex('O1')
            
            if (i > -1 and j == i+1 and k == j+1) or (k > -1 and j == k+1 and i == j + 1):
                self.grammar[11] = 1

    
    #13th parameter
    def questionInver(self):
        if 'ka' in self.infoList[2]: self.grammar[12] = 0
