from time import time
from sys import argv
from argparse import ArgumentParser
from Child import Child
from runSimulation import runSimulation


def main(argv):
    # The first argument keeps track of the mandatory arguments, number of learners, max number of sentences, and target grammar
    # The second argument is flag that will produce plots for the results
    # The third argument is a flag that will produce csv files for the result's convergence patterns
    parser = ArgumentParser(prog='CUNY Sims', description='Set simulation parameters for learners')
    parser.add_argument('integers', metavar='int', type=int, nargs=3,
                        help='(1) The number of learners (2) The number of sentences consumed (3) The target grammar\'s code')
    parser.add_argument('-p', '--plots', dest='plotFlag', action='store_true',
                        help='Produce pset and convergence time plots for the results')
    parser.add_argument('-c', '--convergence', dest='convergenceFlag', action='store_true',
                        help='Find convergence patterns of the results')

    args = parser.parse_args()
    numLearners = 0
    maxSentences = 0

    # Test whether certain command line arguments
    # can be converted to positive integers
    numLearners = args.integers[0]
    maxSentences = args.integers[1]
    if numLearners < 1 or maxSentences < 1:
        print('Arguments must be positive integers')
        sys.exit(2)


    # Open the file containing sample sentences for
    # English, French, German, and Japanese and read
    # them in a runSimulation class variable along with
    # the chosen target grammar (represented by args.integers[2])
    infoFile = open('EngFrJapGerm.txt','rU')
    runSim1 = runSimulation(infoFile.readlines(), args.integers[2])
    infoFile.close()

    # Choose sentences corresponding to one of the four languages
    # available: French=584, English=611, German=2253, Japanese=3856
    runSim1.makeSelectedSentenceList()


    # Runs a simulation over maxLearners number of eChild learners
    runSim1.runLearners(maxSentences, numLearners, args.convergenceFlag, args.plotFlag)

if __name__ == '__main__':
    start = time()
    main(argv[1:])
    end = time() - start
    print('Time to complete: {}'.format(end))
