from random import choice
from argparse import ArgumentParser
from argparse import ArgumentParser
from NDresults import NDresults
from NDChild import NDChild
from Sentence import Sentence

#GLOBALS
rate = 0.02
conservativerate = 0.01
#numberofsentences = 200000
threshold = .001

infoFile = open('EngFrJapGerm.txt','rU')

def pickASentence(languageDomain):
    return choice(languageDomain)

def createLD(language):
    LD = []
    for line in infoFile:
        [grammStr, inflStr, sentenceStr] = line.split("\t")
        sentenceStr = sentenceStr.rstrip()
        # constructor creates sentenceList
        s = Sentence([grammStr, inflStr, sentenceStr])
        if grammStr == language:
            LD.append(s)
    return LD

if __name__ == '__main__':
    # The argument keeps track of the mandatory arguments,
    #number of learners, max number of sentences, and target grammar
    parser = ArgumentParser(prog='Doing Away With Defaults', description='Set simulation parameters for learners')
    parser.add_argument('integers', metavar='int', type=int, nargs=3,
                        help='(1) The number of learners (2) The number of '
                         'sentences consumed (3) The target grammar\'s code '
                          '(English=611, German=2253, French=584, Japanese=3856)')

    args = parser.parse_args()
    numLearners = 0
    maxSentences = 0

    # Test whether certain command line arguments
    # can be converted to positive integers
    numLearners = args.integers[0]
    numberofsentences = args.integers[1]
    language = args.integers[2]
    if numLearners < 1 or numberofsentences < 1:
        print('Arguments must be positive integers')
        sys.exit(2)

    ndr = NDresults()
    ndr.writeOutputHeader(language, numLearners, numberofsentences)

    for i in range(numLearners):
        LD = createLD(str(language))
        print(LD)
        aChild = NDChild(rate, conservativerate)

        for j in range(numberofsentences):
            s = pickASentence(LD)
            aChild.consumeSentence(s)
            ndr.checkIfParametersMeetThreshold(threshold, aChild.grammar, j)

        ndr.writeResults(aChild.grammar, i)
        print aChild.grammar

    infoFile.close()
