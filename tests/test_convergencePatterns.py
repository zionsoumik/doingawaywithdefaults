from ..convergencePatterns import convergencePatterns
from ..Child import Child
import random
import pytest
from collections import defaultdict
import os.path
import shutil
from itertools import permutations

# Make a convergencePatterns object instance
# for use in the test functions
patterns = convergencePatterns.convergencePatterns('./results/test_path')

'''
Checks that there is a value greater than zero
within all possible dictionary key pairs.
The function will check for pairings with currKey and
any paired key must appear after it in timeCourseVector
'''
def checkForKeyPairs(currKeyIndex, timeCourseVector, dict):
    currKey = timeCourseVector[currKeyIndex][1]

    for i in range(1, 13):
        secondKey = timeCourseVector[i][1]
        if i > currKeyIndex:
            assert dict[currKey][secondKey] > 0
        else:
            print('Ahoy')
            #assert not secondKey in dict[currKey]


'''
Checks that valid triple key groups are present in dict and that
the value is greater than zero
'''
def checkForKeyTrios(currKeyIndex, secondKeyIndex, timeCourseVector, dict):
        assert currKeyIndex < secondKeyIndex
        currKey = timeCourseVector[currKeyIndex][1]
        secondKey = timeCourseVector[secondKeyIndex][1]

        for i in range(1, 13):
                thirdKey = timeCourseVector[i][1]
                if i > secondKeyIndex:
                        assert dict[currKey][secondKey][thirdKey] > 0
                        print("ck: {0}, sk: {1}, tk: {2}".format(currKey, secondKey, thirdKey))
                else:
                        assert not thirdKey in dict[currKey][secondKey]


'''
Checks that valid triple key groups are present in dict and that
the value is greater than zero
'''
def checkForKeyQuartets(currKeyIndex, secondKeyIndex, thirdKeyIndex, timeCourseVector, dict):
        assert currKeyIndex < secondKeyIndex < thirdKeyIndex
        currKey = timeCourseVector[currKeyIndex][1]
        secondKey = timeCourseVector[secondKeyIndex][1]
        thirdKey = timeCourseVector[thirdKeyIndex][1]

        for i in range(1, 13):
                fourthKey = timeCourseVector[i][1]
                if i > thirdKeyIndex:
                        assert dict[currKey][secondKey][thirdKey][fourthKey] > 0
                        print("ck: {0}, sk: {1}, tk: {2}, fk: {3}".format(currKey, secondKey, thirdKey, fourthKey))
                else:
                        assert not fourthKey in dict[currKey][secondKey][thirdKey]


'''
Create a time course vector for testing.
The first element of each inner list represents the
time at which the parameter converged. The second 
element indicates the specific parameter by number
'''
def test_convergenceQuartetsDictEntries():
        # Make a sample dictionary, that will contain a number of dictionaries
        # of varying levels, and a sample time course vector
        sampleTCV = [[3, 5], [4, 1], [10, 12], [11, 11], [14, 2], [14, 8], [24, 3], [26, 6], [30, 4], [31, 9], [56, 7], [60, 13], [61, 10]]

        patterns.findQuartetConvergencePatterns(sampleTCV)
        for i in range(0, 11):
                for j in range(i+1, 12):
                        for k in range(j+1, 13):
                                checkForKeyQuartets(i, j, k, sampleTCV, patterns.quartetDict)


'''
Create a tcv and dictionary containing random integers
representing convergence times between one and five inclusive
Use these structures with findQuartetConvergencePatterns
to test whether the function can handle this
'''
def randomTesting():
        # Create a time course vector for testing.
        # The first element be random, inclusive number between one and five
        sampleTCV = []
        for i in range(1, 14):
                sampleTCV.append([randit(1, 5), i])

        # Make a sample dictionary, that will contain a number of dictionaries
        # of varying levels
        sampleDict = {randit(1, 5) : {}, randit(1, 5) : {randit(1, 5) : {randit(1, 5) : {}}}, randit(1, 5) : {randit(1, 5) : {}}}

        # Run the function to insure it can handle random entries in sampleTCV and sampleDict
        findQuartetConvergencePatterns(sampleDict, sampleTCV, 1, 11, 3)


'''
Runs findConvergencePatterns with a sample dictionarie and time course vector.
Afterwords, checkForKeyPairs will test the contents of sampleDict to see if 
appropriate key pairs and values were added. py.test should be used to run these
tests
'''
def test_inOrderTCV():
        c1 = Child.Child()
        c1.timeCourseVector = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10], [11, 11], [12, 12], [13, 13]]
        sampleChildList = [c1]

        patterns.findConvergencePairs(c1.timeCourseVector)
        
        ''' 
        After running findConvergencePatterns, sampleDict should contain a number of key
        and inner key pairs. The outer key should always appear before the inner key in the
        sample time course vector
        Every parameter is checked in the for loop 
        '''
        for i in range(0, 13):
                checkForKeyPairs(i, c1.timeCourseVector, patterns.pairDict)


def test_getHeader():
        c = convergencePatterns.convergencePatterns('test_output.csv')
        x= c.getHeader(2)
        print(x)


def makeQuartetDict():
        quartetDict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0))))
        permList = list(permutations(range(1,14),4))
        for index, perm in enumerate(permList):
                quartetDict[perm[0]][perm[1]][perm[2]][perm[3]] = index
        return quartetDict


def makePairDict():
        pairDict = defaultdict(lambda: defaultdict(lambda: 0))
        permList = list(permutations(range(1,14),2))
        for index, perm in enumerate(permList):
                pairDict[perm[0]][perm[1]] = index
        return pairDict

def test_getPairDictTotal():
        patterns.pairDict = makePairDict()
        permList = list(permutations(range(1,14),2))
        for index, perm in enumerate(permList):
                print(patterns.getPairTotal2(perm))
                assert index == patterns.getPairDictTotal(perm)


def test_writeQuartetResults():
        patterns.writeQuartetResults()
        outputFilePath = os.path.join(patterns.outputPath+'_quartetConvergenceResults.csv')
        assert os.path.isfile(outputFilePath)
        shutil.rmtree('./results')
        assert not os.path.isfile(outputFilePath)


def test_writeTrioResults():
        patterns.writeTrioResults()
        patterns.outputPath = './results/test_path3'
        outputFilePath = os.path.join(patterns.outputPath+'_TrioConvergenceResults.csv')
        assert os.path.isfile(outputFilePath)
        shutil.rmtree('./results')
        assert not os.path.isfile(outputFilePath)


def test_writePairResults():
        patterns.writePairResults()
        patterns.outputPath = './results/test_path2'
        outputFilePath = os.path.join(patterns.outputPath+'_PairConvergenceResults.csv')
        assert os.path.isfile(outputFilePath)
        shutil.rmtree('./results')
        assert not os.path.isfile(outputFilePath)

