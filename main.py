from time import time
from random import choice
from argparse import ArgumentParser
from argparse import ArgumentParser
from NDresults import NDresults
from NDChild import NDChild
from Sentence import Sentence

#GLOBALS
rate = 0.02
conservativerate = 0.001
threshold = .001

def pickASentence(languageDomain):
    return choice(languageDomain)

def createLD(language):
    languageDict = {'english': '611', 'french': '584', 'german': '2253', 'japanese': '3856'}
    langNum = languageDict[language]
    LD = []

    with open('EngFrJapGerm.txt','r') as infoFile:
        for line in infoFile:
            [grammStr, inflStr, sentenceStr] = line.split("\t")
            sentenceStr = sentenceStr.rstrip()
            # constructor creates sentenceList
            s = Sentence([grammStr, inflStr, sentenceStr])
            if grammStr == langNum:
                LD.append(s)

    return LD

def runOneLanguage(numLearners, numberofsentences, language):
    if numLearners < 1 or numberofsentences < 1:
        print('Arguments must be positive integers')
        sys.exit(2)

    # Make an instance of NDresults and write the header for the output file
    ndr = NDresults()
    ndr.writeOutputHeader(language, numLearners, numberofsentences)

    LD = createLD(language)
    results = []
    print("Starting the simulation...")
    for i in xrange(numLearners):
        ndr.resetThresholdDict()
        aChild = NDChild(rate, conservativerate)

        for j in xrange(numberofsentences):
            s = pickASentence(LD)
            aChild.consumeSentence(s)
            # If a parameter value <= to the threshold for the first time,
            # this is recorded in ndr for writing output
            ndr.checkIfParametersMeetThreshold(threshold, aChild.grammar, j)

        results.append([aChild.grammar, ndr.thresholdDict])
        print "Finished Child {}".format(i)
    ndr.writeResults(results)

# Run random 100 language speed run
def runSpeedTest(numLearners, numberofsentences):
    # Make dictionary containing first 100
    # language IDs from the full CoLAG domain

    '''
    with open('COLAG_Flat_GrammID_Binary_List.txt','r') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    for i in range(0, 100):
        binaryId, decimalId = content[i].split('\t')
        languageDict[binaryId] = []
    '''
    languageDict = {}
    with open('COLAG_Flat_GrammID_Binary_List.txt','r') as myfile:
        head = [next(myfile) for x in xrange(100)]

    for line in head:
        binaryId, decimalId = line.split('\t')
        languageDict[binaryId] = []

    # Collect the corresponding sentences for each language
    with open('COLAG_2011_flat_formatted.txt', 'r') as infoFile:
        for line in infoFile:
            [grammStr, inflStr, sentenceStr] = line.split("\t")

            if grammStr in languageDict:     
                sentenceStr = sentenceStr.rstrip()
                # constructor creates sentenceList
                s = Sentence([grammStr, inflStr, sentenceStr])
                languageDict[grammStr].append(s)

    '''
    with open('EngFrJapGerm.txt','r') as infoFile:
        for line in infoFile:
            [grammStr, inflStr, sentenceStr] = line.split("\t")
            sentenceStr = sentenceStr.rstrip()
            # constructor creates sentenceList
            s = Sentence([grammStr, inflStr, sentenceStr])
            if grammStr == langNum:
                LD.append(s)
    '''


    # Run 100 eChildren for each language
    for key, value in languageDict.iteritems():
        language = str(int(key, 2))
        ndr = NDresults()
        ndr.writeOutputHeader(language, numLearners, numberofsentences)

        results = []
        print("Starting the simulation...")
        for i in xrange(numLearners):
            ndr.resetThresholdDict()
            aChild = NDChild(rate, conservativerate)

            for j in xrange(numberofsentences):
                s = pickASentence(value)
                aChild.consumeSentence(s)
                # If a parameter value <= to the threshold for the first time,
                # this is recorded in ndr for writing output
                ndr.checkIfParametersMeetThreshold(threshold, aChild.grammar, j)

            results.append([aChild.grammar, ndr.thresholdDict])
            print "Finished Child {}".format(i)
        ndr.writeResults(results)


if __name__ == '__main__':
    start = time()

    # The argument keeps track of the mandatory arguments,
    #number of learners, max number of sentences, and target grammar
    parser = ArgumentParser(prog='Doing Away With Defaults', description='Set simulation parameters for learners')
    parser.add_argument('integers', metavar='int', type=int, nargs=2,
                        help='(1) The number of learners (2) The number of '
                         'sentences consumed')
    parser.add_argument('strings', metavar='str', type=str, nargs=1,
                        help='The name of the language that will be used.'
                                'The current options are English=611, '
                                'German=2253, French=584, Japanese=3856')

    args = parser.parse_args()
    numLearners = 0
    maxSentences = 0

    # Test whether certain command line arguments
    # can be converted to positive integers
    numLearners = args.integers[0]
    numberofsentences = args.integers[1]
    language = str(args.strings[0]).lower()

    #runOneLanguage(numLearners, numberofsentences, language)
    runSpeedTest(numLearners, numberofsentences)

    print("--- %s seconds ---" % (time() - start))
