#!/opt/anaconda/bin/python

'''
The following will produce a line graph representing
the order (represented by p-set) in which each learner's
parameters converged
'''

# Standard import for pandas, numpy and matplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys


# Used to store the input file whose contents will be analyzed
inputFile = ''

if sys.argv[1].endswith('csv'):
        inputFile = sys.argv[1]
else:
    print('The name of the input file must end with the .csv extension')
    sys.exit(2)

# Import and view data from inputFile
df = pd.read_csv(inputFile)
df.head()


# Get the number of rows in the dataframe
numLearners = df.shape[0]

# Create a list of lists, each inner list represents
# a parameter and the sentence on which it converged on
rowList = []
for i in range(0, numLearners):
    # Use iloc to grab a row
    # and convert it to a list
    l = list(df.iloc[[i]].values.flatten())
    dbList = []
    for j in range(0, 13):
        dbList.append([l[j], j+1])
    dbList.sort(key=lambda x: x[0])
    rowList.append(dbList)


# Returns one of five colors based on the current
# numbers's last digit. This will be assigned
# to a line in the graph representing a learner
def get_line_color(num):
    lastDigit = num % 10
    if lastDigit == 0 or lastDigit == 5:
        return "blue"
    elif lastDigit == 1 or lastDigit == 6:
        return "green"
    elif lastDigit == 2 or lastDigit == 7:
        return "red"
    elif lastDigit == 3 or lastDigit == 8:
        return "yellow"
    else: # lastDigit == 4 or lastDigit == 9
        return "purple"


# Stores every completed line that will appear
# on the graph
data = []
for i in range(0, numLearners):
    # Variables used to store the x-axis
    # and y axis data of each learner
    xData = []
    yData = []
    
    # The appropiate data is added,
    # xData stores the p-set of each parameter
    # yData stores the corresponding parameter number
    psetCounter = 1
    currentConvergenceTime = rowList[i][0][0]
    for j in range(0, 13):
        if rowList[i][j][0] != currentConvergenceTime:
            psetCounter += 1
            currentConvergenceTime = rowList[i][j][0]
        xData.append(psetCounter)
        yData.append(rowList[i][j][1])
    
    data.append(xData)
    data.append(yData)
    data.append(get_line_color(i))


# Create a figure of size 8x6 inches, 80 dots per inch
plt.figure(figsize=(8, 6), dpi=80)

# Add graph title and axis labels
plt.title("P-sets of Parameters")
plt.xlabel("P-set")
plt.ylabel("Parameters")

for i in range(0, numLearners, 3):
    plt.plot(data[i], data[i+1], color=data[i+2], linewidth=1.0, marker='.', linestyle="-")

# Set x limits
plt.xlim(0, 13)

# Set x ticks
plt.xticks(np.linspace(0, 13, 14, endpoint=True))

# Set y limits
plt.ylim(1, 13)

# Set y ticks
plt.yticks(np.linspace(1, 13, 13, endpoint=True))

# Save the resulting graph as a pdf
figure = plt.gcf()
figure.savefig(inputFile[:-4] + '_pset.pdf')
