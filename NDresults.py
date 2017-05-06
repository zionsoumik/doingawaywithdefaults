class NDResults(object):
    def __init__ (self):
        self.metThreshold = {"SP": False, "HIP": False, "HCP": False, "OPT": False, "NS": False, "NT": False, "WHM": False, "PI": False, "TM": False, "VtoI": False, "ItoC": False, "AH": False, "QInv": False}
        self.thresholdDict = {"SP": 0, "HIP": 0, "HCP": 0, "OPT": 0, "NS": 0, "NT": 0, "WHM": 0, "PI": 0, "TM": 0, "VtoI": 0, "ItoC": 0,"AH": 0, "QInv": 0}

    def checkIfParametersMeetThreshold(self, threshold, grammar, currSentenceNum):
        for key, value in grammar.iteritems():
            if not metThreshold[key] and value <= threshold:
                self.thresholdDict[key] = currSentenceNum
                self.metThreshold[key] = True


    # Write the header columns to the output file
    def writeOutputHeader(self, language_code, numEChildren, numSentences):
        languageDict = {611:'English', 584:'French', 2253:'German', 584:'Japanese'}
        with open('output-simulation.csv',"a+") as outFile:
            writer = csv.writer(outFile)
            r1 = str(languageDict[language_code]) + str(language_code)
            writer.writerow([r1])
            r2 = "{} eChildren".format(numEChildren)
            writer.writerow([r2])
            r3 = "{} sentences".format(numSentences)
            writer.writerow([r3])
            pList = ["SP", "HIP", "HCP", "OPT", "NS", "NT", "WHM", "PI", "TM", "VtoI", "ItoC","AH", "QInv"]
            r4 = [' '] + ['{}'.format(p) for p in pList]
            print(r4)
            writer.writerow(r4)


    # Writes the final grammar and time (particular sentence) that each
    # parameter of each eChild converged on to the output file
    def writeResults(self, grammar, num):
        with open('output-simulation.csv',"a+") as outFile:
            writer = csv.writer(outFile)
            str1 = 'eChild {}'.format(num)
            pList = ["SP", " ", "HIP", " ", "HCP", " ", "OPT", " ", "NS", " ", "NT", " ", "WHM", " ", "PI",
                 ' ', "TM", " ", "VtoI", " ", "ItoC", " ", "AH", " ", "QInv", " "]
            r1 = [str1]
            for p in pList:
                r1.append(format(grammar[p], '.12f'))
                r1.append(thresholdDict[p])
                writer.writerow(r1)
