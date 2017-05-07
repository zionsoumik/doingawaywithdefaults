class NDResults(object):
    def __init__ (self):
        self.thresholdDict = {"SP": -1, "HIP": -1, "HCP": -1, "OPT": -1, "NS": -1, "NT": -1, "WHM": -1, "PI": -1, "TM": -1, "VtoI": -1, "ItoC": -1,"AH": -1, "QInv": -1}

    def checkIfParametersMeetThreshold(self, threshold, grammar, currSentenceNum):
        for key, value in grammar.iteritems():
            if thresholdDict[key] < 0 and value <= threshold:
                self.thresholdDict[key] = currSentenceNum


    # Write the header columns to the output file
    def writeOutputHeader(self, language_code, numEChildren, numSentences):
        # Delete the old version of the output file
        os.remove('output-simulation.csv')

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
