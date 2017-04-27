from Child import Child
from collections import defaultdict
import csv
from itertools import chain, permutations
from os import path
from math import floor


class convergencePatterns(object):
        def __init__(self, op):
                # Each defaultdict is used to store every pair, trio, and quartet of parameter convergence orders
                # found in the learners.
                self.outputPath = op
                self.pairDict = defaultdict(lambda: defaultdict(lambda: 0))
                self.trioDict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
                self.quartetDict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0))))

        
        # Creates column headers for each output file
        # Will print every possible permutation for the
        # chosen number of parameters for comparison
        def getHeader(self, n):
            columnHeader = 'p{}' + ' < p{}' * (n-1)
            perms = (list(permutations(range(1,14), n)))
            f = lambda perms: columnHeader.format(*perms)
            return list(map(f, perms))


        # 156 total permutations
        def writePairResults(self):
                outFile = path.join(self.outputPath + '_PairConvergenceResults.csv')
                with open(outFile, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(self.getHeader(2))
                        perms = list(permutations(range(1,14),2))
                        k = lambda perm: self.pairDict[perm[0]][perm[1]]
                        writer.writerow(list(map(k,perms)))


        '''
        Will record the number of times each threesome permutation of parameters 1-13
        occurs. Since the total number of permutations exceed the cell limit of a row,
        the header and results will be printed to multiple rows
        '''
        def writeTrioResults(self):
                outFile = path.join(self.outputPath + '_TrioConvergenceResults.csv')
                with open(outFile, 'a') as f:
                        writer = csv.writer(f)
                        header = self.getHeader(3)
                        perms = list(permutations(range(1,14),3))
                        k = lambda perm: self.trioDict[perm[0]][perm[1]][perm[2]]
                        writer.writerow(header[:1024])
                        writer.writerow(list(map(k, perms[:1024])))
                        writer.writerow(header[1024:])
                        writer.writerow((map(k, perms[1024:])))


        '''
        Will record the number of times each foursome permutation of parameters 1-13
        occurs. Since the total number of permutations exceed the cell limit of a row,
        the header and results will be printed to multiple rows
        '''
        def writeQuartetResults(self):
                outFile = path.join(self.outputPath + '_QuartetConvergenceResults.csv')
                with open(outFile, 'a') as f:
                        writer = csv.writer(f)
                        header = self.getHeader(4)
                        perms = list(permutations(range(1,14),4))
                        numberOfRows = floor(len(perms) / 1024)
                        startIndex = 0
                        endIndex = 1024
                        k = lambda perm: self.quartetDict[perm[0]][perm[1]][perm[2]][perm[3]]
                        for i in range(numberOfRows):
                                writer.writerow(header[startIndex:endIndex])
                                writer.writerow(list(map(k,perms[startIndex:endIndex])))
                                startIndex = endIndex + 1
                                endIndex = startIndex + 1024


        def writeResults(self):
                self.writePairResults()
                print('Pair results written to file')

                self.writeTrioResults()
                print('Trio results written to file')

                self.writeQuartetResults()
                print('Quartet results written to file')


        # Will check for different sentence convergence foursome
        # combinations exist. Different combinations are added to quarterDict
        # if they don't appear, otherwise the count within their corresponding
        # dictionary entry is incremented
        def findQuartetConvergencePatterns(self, sortedTCV):
                countTrio = False
                countPair = False
                for i in range(0, 13):
                        for j in range(i+1, 13):
                                firstParameter = sortedTCV[i][1]
                                secondParameter = sortedTCV[j][1]
                                self.pairDict[firstParameter][secondParameter] += 1
                                for k in range(j+1, 13):
                                        thirdParameter = sortedTCV[k][1]
                                        self.trioDict[firstParameter][secondParameter][thirdParameter] += 1
                                        for l in range(k+1, 13):
                                                self.quartetDict[firstParameter][secondParameter][thirdParameter][sortedTCV[l][1]] += 1


        # Will track the different convergence patterns (the order in which each parameter converges)
        # that appear in a learner's time course vector.
        # Currently, it will track pairs, triplets, and quartets of parameter combinations
        def findConvergencePatterns(self, tcvList):
                for tcv in tcvList:
                        # Sort the learner's timeCourseVector based on the convergence
                        # time of each parameter
                        sortedTCV = sorted(tcv, key=lambda parameter: parameter[0])
                        self.findQuartetConvergencePatterns(sortedTCV)
                self.writeResults()
