from Child import Child
from convergencePatterns import convergencePatterns
from time import clock
from random import choice
import csv
from datetime import datetime
import os

class runSimulation(object):
    def __init__(self, si, lc):
        self.totalSentenceCount = 0.0
        self.totalConvergentChildren = 0.0
        self.sentenceInfo = si
        self.targetGrammar = lc
        self.selectedSentences = []
        self.outputFile = ''

    # Prints the percentage of converged children
    # and the average sentence count of converged children
    def printResults(self, maxChildren):
        try:
            print('Percentage of converged children: '), (self.totalConvergentChildren / maxChildren) * 100, '%'
        except ZeroDivisionError:
            print('Zero Error')

        try:
            print('Average sentence count of converged children: '), (self.totalSentenceCount / self.totalConvergentChildren)
        except ZeroDivisionError:
            print('Average sentence count of converged children: 0')


    # Write the header columns to the output file
    def writeOutputHeader(self):
        with open(self.outputFile,"a+") as outFile:
            writer = csv.writer(outFile)
            writer.writerow(('TCV', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Grammar'))
            writer.writerow(['p{}'.format(i) for i in range(1,14)] * 2)


    # Writes the final grammar and time (particular sentence) that each
    # parameter of each eChild converged on to the output file
    def writeResults(self, grammarList, tcvList):
        with open(self.outputFile,"a+") as outFile:
            writer = csv.writer(outFile)

            for i in range(len(grammarList)):
                writer.writerow( (tcvList[i][0][0], tcvList[i][1][0], tcvList[i][2][0], tcvList[i][3][0], tcvList[i][4][0], tcvList[i][5][0],
                tcvList[i][6][0], tcvList[i][7][0], tcvList[i][8][0], tcvList[i][9][0], tcvList[i][10][0], tcvList[i][11][0], tcvList[i][12][0],
                grammarList[i][0], grammarList[i][1], grammarList[i][2], grammarList[i][3], grammarList[i][4], grammarList[i][5], grammarList[i][6],
                grammarList[i][7], grammarList[i][8], grammarList[i][9], grammarList[i][10], grammarList[i][11], grammarList[i][12]) )


    # Fills runSimulation object's selectedSentences array with sentences who
    # belong to the language that correspond to targetGrammar
    def makeSelectedSentenceList(self):
        lc = str(self.targetGrammar)
        for i in range(0, len(self.sentenceInfo)):
            # Get the code from the current sentence and compare it to lc
            if self.sentenceInfo[i].split('\t', 1)[0] == lc:
                self.selectedSentences.append(self.sentenceInfo[i])


    # Returns the name of the language
    # that languageCode corresponds to
    def getLanguage(self):
        if self.targetGrammar == 611:
            return 'English'
        elif self.targetGrammar == 584:
            return 'French'
        elif self.targetGrammar == 2253:
            return 'German'
        elif self.targetGrammar == 3856:
            return 'Japanese'
        elif self.targetGrammar == 547 or self.targetGrammar == 227 or self.targetGrammar == 867 or self.targetGrammar == 35 or self.targetGrammar == 163 or self.targetGrammar == 803:
            return 'English_Superset_{}'.format(self.targetGrammar)


    # The child, or learner, processes sentences belonging to the chosen language
    # until its grammar is identical to the language's or it has processed the
    # chosen number of sentences (maxSentences). The timeCourseVector data of the
    # learner is then written to the output file
    def doesChildLearnGrammar(self, eChild, maxSentences):
        start = clock()

        while not eChild.grammarLearned and eChild.sentenceCount < maxSentences:
            eChild.consumeSentence(choice(self.selectedSentences))
            eChild.setParameters()
            eChild.sentenceCount += 1

        totalTime = clock() - start

        # Write the grammar and time course vector to an output file
        # Return the time course vector so it can be used to find convergence patterns
        return [eChild.grammar, eChild.timeCourseVector]

    # Runs a simulation containing maxLearners number of learners
    # Each learner runs the doesChildLearnGrammar function and processes
    # sentences with the chosen constraints
    def runLearners(self, maxSentences, maxLearners, convergenceFlag, plotFlag):
        # Create the name and path of the output file
        baseName = self.getLanguage() + '_' + str(maxLearners)  + '_' + datetime.now().isoformat().replace(':','.')

        tempPathName = './results/{}'.format(baseName)
        tempFileName = baseName + '_grammar_tcv.csv'
        os.makedirs(tempPathName)
        self.outputFile = os.path.join(tempPathName, tempFileName)
        self.writeOutputHeader()

        # Stores the grammars and time course vectors of each learner after
        # processing the specified number of sentences
        grammarList = []
        tcvList = []

        for i in range(1, maxLearners+1):
            childResults = self.doesChildLearnGrammar(Child(), maxSentences)
            #tcvList.append(self.doesChildLearnGrammar(Child(), maxSentences))
            grammarList.append(childResults[0])
            tcvList.append(childResults[1])
            print('Finished #{}'.format(i))
        self.writeResults(grammarList, tcvList)

        # If convergenceFlag is set to true, make a convergencePatterns instance
        # and find resulting convergence patterns
        if convergenceFlag:
            print('Making convergence pattern files...')
            patterns = convergencePatterns(self.outputFile[:-7])
            patterns.findConvergencePatterns(tcvList)

        # If plotFlag is set to true, corresponding plots are produced and saved
        if plotFlag:
            print('Making pset and convergence time plots...')
            os.system("./pset_plot.py {}".format(self.outputFile))
            os.system("./convergenceTime_plot.py {}".format(self.outputFile))

        print('Finished simulation')
