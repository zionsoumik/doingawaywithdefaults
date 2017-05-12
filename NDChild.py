class NDChild(object):
    def __init__ (self, learningrate, conslearningrate):

        self.grammar = {"SP": .5, "HIP": .5, "HCP": .5, "OPT": .5, "NS": .5, "NT": .5,"WHM": .5, "PI": .5, "TM": .5, "VtoI": .5, "ItoC": .5,"AH": .5, "QInv": .5}
        self.r = learningrate #simulation will pass child a learning rate
        self.conservativerate = conslearningrate

    def consumeSentence(self, s): #child is fed a list containing [lang, inflec, sentencestring]
        self.spEtrigger(s)    #parameter 1
        self.hipEtrigger(s)   #parameter 2
        self.hcpEtrigger(s)   #parameter 3
        #self.optEtrigger(s)  #parameter 4
        self.nsEtrigger(s)    #parameter 5
        self.ntEtrigger(s)    #parameter 6
        self.whmEtrigger(s)   #parameter 7
        self.piEtrigger(s)    #parameter 8
        self.tmEtrigger(s)    #parameter 9
        self.VtoIEtrigger(s)  #parameter 10
        #self.ItoCEtrigger(s) #parameter 11
        self.ahEtrigger(s)    #parameter 12
        #self.QInvEtrigger(s) #parameter 13

    #etriggers for parameters
    # first parameter Subject Position
    def spEtrigger(self, s):
        # Check if O1 and S are in the sentence and sent is declarative
        if "O1" in s.sentenceList and "S" in s.sentenceList and s.inflection == "DEC":
            O1index = s.sentenceList.index("O1")
            # Make sure O1 is non-sentence-initial and before S
            if O1index > 0 and O1index < s.sentenceList.index("S"):
                # set towards Subject final
                self.adjustweight ("SP",1, self.r)
            # S occurs before 01
            elif O1index > 0 and O1index > s.sentenceList.index("S"):
                # set towards Subject initial
                self.adjustweight("SP",0,self.r)

    # second parameter Head IP, VP, PP, etc
    def hipEtrigger(self, s):
        if "O3" in s.sentenceList and "P" in s.sentenceList:
            O3index = s.sentenceList.index("O3")
            Pindex = s.sentenceList.index("P")
            # O3 followed by P and not topicalized
            if O3index > 0 and Pindex == O3index + 1:
                self.adjustweight ("HIP", 1, self.r)
            elif O3index > 0 and Pindex == O3index - 1:
                self.adjustweight ("HIP", 0, self.r)

        # If imperative, make sure Verb directly follows O1
        elif s.inflection == "IMP" and "O1" in s.sentenceList and "Verb" in s.sentenceList:
            if s.sentenceList.index("O1") == s.sentenceList.index("Verb") - 1:
                self.adjustweight ("HIP", 1, self.r)
            elif s.sentenceList.index("Verb") == (s.sentenceList.index("O1") - 1):
                self.adjustweight("HIP", 0, self.r)

    # third parameter Head in CP
    def hcpEtrigger(self, s):
        if s.inflection == "Q":
            # ka or aux last in question
            if s.sentenceList[-1] == 'ka' or ("ka" not in s.sentenceList and s.sentenceList[-1] == "Aux"):
                self.adjustweight("HCP", 1, self.r)
            # ka or aux first in question
            elif s.sentenceList[0] == "ka" or ("ka" not in s.sentenceList and s.sentenceList[0]=="Aux"):
                self.adjustweight("HCP", 0, self.r)

    def nsEtrigger(self, s):
        if s.inflection == "DEC" and "S" not in s.sentenceStr and s.outOblique():
            self.adjustweight("NS",1,self.r)
        elif s.inflection == "DEC" and "S" in s.sentenceStr and s.outOblique():
            self.adjustweight("NS",0,self.conservativerate)

    def ntEtrigger(self, s):
        if s.inflection == "DEC" and "O2" in s.sentenceStr and "O1" not in s.sentenceStr:
            self.adjustweight("NT",1,self.r)

        elif s.inflection == "DEC" and "O2" in s.sentenceStr and "O1" in s.sentenceStr and "O3" in s.sentenceStr and "S" in s.sentenceStr and "Adv" in s.sentenceStr:
            self.adjustweight("NT",0,self.conservativerate)
        #if all possible complements of VP are in sentence, then the sentence is not Null Topic

    def whmEtrigger(self, s):
        if s.inflection == "Q" and "+WH" in s.sentenceStr:
            if ("+WH" in s.sentenceList[0]) or ("P" == s.sentenceList[0] and "O3[+WH]" == s.sentenceList[1]):
                self.adjustweight("WHM",1,self.conservativerate)
            else:
                self.adjustweight("WHM",0,self.r)

    def piEtrigger(self, s):
        if "P" in s.sentenceList and "O3" in s.sentenceList:
            if abs(s.indexString("P") - s.indexString("O3")) > 1:
                self.adjustweight("PI", 1, self.r)

            elif ((s.indexString("P") + s.indexString("O3")) == 1):
                self.adjustweight ("PI",0,self.r)

    def tmEtrigger(self, s):
        if "[+WA]" in s.sentenceStr:
            self.adjustweight("TM",1,self.r)
        elif "O1" in s.sentenceList and "O2" in s.sentenceList and (abs(s.sentenceList.index("O1")-s.sentenceList.index("O2")) > 1):
            self.adjustweight("TM",0,self.r)

    def VtoIEtrigger(self, s):
        if "Verb" in s.sentenceList and "O1" in s.sentenceList:
            o1index = s.indexString("O1")
            if o1index != 0 and abs(s.indexString("Verb") - o1index) > 1:
                self.adjustweight("VtoI", 1, self.r)
                self.adjustweight("AH", 0, self.r)

        #no need to explicitly check inflection because only Q and DEC have AUX
        elif "Aux" in s.sentenceList:
            self.adjustweight("VtoI", 0, self.conservativerate)


    def ItoCEtrigger(self, s):
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

    def ahEtrigger(self, s):
        if (s.inflection == "DEC" or s.inflection == "Q") and ("Aux" not in s.sentenceStr and "Never" in s.sentenceStr and "Verb" in s.sentenceStr and "O1" in s.sentenceStr):
            neverPos = s.indexString("Never")
            verbPos = s.indexString("Verb")
            O1Pos = s.indexString("O1")

            if (neverPos > -1 and verbPos == neverPos+1 and O1Pos == verbPos+1) or (O1Pos > -1 and verbPos == O1Pos+1 and neverPos == verbPos + 1):
                self.adjustweight("AH", 1, self.r)
                self.adjustweight("VtoI", 0, self.r)

        elif "Aux" in s.sentenceStr and self.grammar["AH"] <= 0.5:
            self.adjustweight ("AH",0,self.conservativerate)

    def adjustweight(self, parameter, direction, rate):
        if direction == 0:
            self.grammar[parameter] -= rate*self.grammar[parameter]
        elif direction == 1:
            self.grammar[parameter] += rate*(1-self.grammar[parameter])
