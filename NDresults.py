from csv import writer
from os import remove, path

class NDresults(object):
    def __init__ (self):
        self.thresholdDict = {"SP": -1, "HIP": -1, "HCP": -1, "OPT": -1, "NS": -1, "NT": -1, "WHM": -1, "PI": -1, "TM": -1, "VtoI": -1, "ItoC": -1,"AH": -1, "QInv": -1}

    # Check if the threshold hasn't been met before and if so, check if current
    # parameter value meets it
    def checkIfParametersMeetThreshold(self, threshold, grammar, currSentenceNum):
        for key, value in grammar.iteritems():
            if self.thresholdDict[key] < 0 and (value <= threshold or value >= (1-threshold)):
                self.thresholdDict[key] = currSentenceNum


    # Write the header columns to the output file
    def writeOutputHeader(self, language_code, numEChildren, numSentences):
        # Delete the old version of the output file if it exists
        if path.exists('output-simulation.csv'):
            remove('output-simulation.csv')

        languageDict = {611:'English', 584:'French', 2253:'German', 3856:'Japanese'}
        with open('output-simulation.csv',"a+") as outFile:
            outWriter = writer(outFile)
            r1 = str(languageDict[language_code]) + str(language_code)
            outWriter.writerow([r1])
            r2 = "{} eChildren".format(numEChildren)
            outWriter.writerow([r2])
            r3 = "{} sentences".format(numSentences)
            outWriter.writerow([r3])
            pList = ["SP", " ", "HIP", " ", "HCP", " ", "OPT", " ", "NS", " ", "NT", " ", "WHM", " ", "PI",
                             ' ', "TM", " ", "VtoI", " ", "ItoC", " ", "AH", " ", "QInv", " "]
            r4 = [' '] + ['{}'.format(p) for p in pList]
            outWriter.writerow(r4)


    # Writes the final grammar and time (particular sentence) that each
    # parameter of each eChild converged on to the output file
    def writeResults(self, grammar, num):
        with open('output-simulation.csv',"a+") as outFile:
            outWriter = writer(outFile)
            str1 = 'eChild {}'.format(num)
            pList = ["SP", "HIP", "HCP", "OPT", "NS", "NT", "WHM", "PI", "TM", "VtoI", "ItoC","AH", "QInv"]
            r1 = [str1]
            for p in pList:
                # Add the parameter value and at what sentence it met the threshold
                r1.append(format(grammar[p], '.12f'))
                r1.append(self.thresholdDict[p])
            outWriter.writerow(r1)
