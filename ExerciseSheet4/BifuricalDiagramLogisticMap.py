import numpy as np
import matplotlib.pyplot as plt
import random

# This Script calculates logistical map sequences and can produce bifurcation diagrams of those sequences


class logMapClass():  # data for one logistic map sequence

    x_0 = 0.9                           # first element of the sequence
    mu = 0                              # mu of the logistic map
    seqLength = 100                     # the length of
    logMapSeq = np.zeros(seqLength)     # sequence produced by the logistic map

    def __init__(self, x_0, mu, seqLength):  # class constructor
        self.x_0 = x_0
        self.mu = mu
        self.seqLength = seqLength

        self.setLogMapSeq()

    # set the sequence of the logistic map till N
    def setLogMapSeq(self):
        self.logMapSeq = np.zeros(self.seqLength)
        # set the first element of the sequence to x_0
        self.logMapSeq[0] = self.x_0

        # go through each element of the logistic map and calculate the new element from the old
        for i in range(0, self.seqLength - 1):
            self.logMapSeq[i + 1] = self.logMapSeq[i] * \
                self.mu*(1 - self.logMapSeq[i])

    def plot(self):
        plt.plot(self.logMapSeq)
        plt.xlabel("Element in Sequence")
        plt.ylabel("x")
        plt.show()


# set plot data for the bifurical diagram
class bifuricalDiagramPlotData(logMapClass):
    seqLength = 200         # length of the logistic map sequences
    x_0 = random.random()   # first element in the sequence
    intervalParts = 1000    # interval is divided into equal parts
    mu = np.linspace(0, 4, intervalParts)  # elavuation for mu from 0 to 4

    diagramData = np.zeros(intervalParts)

    def __init__(self, seqLength, intervalParts):
        self.seqLength = seqLength
        self.intervalParts = intervalParts
        self.mu = np.linspace(0, 4, self.intervalParts)

        self.setBifuricationDiagramData()

    def setBifuricationDiagramData(self):
        # evaluate the logistic map fosr different values of mu and take the final x-value of each evaluation.
        self.diagramData = np.zeros(self.intervalParts)

        # create a sequence for each mu between 0 and 4
        for i in range(0, self.intervalParts):
            # set the forst element to a random number
            self.x_0 = random.random()
            # create a logistical map sequence with x_0 and mu
            seqData = logMapClass(
                self.x_0, self.mu[i], self.seqLength)
            # keep the last element in the sequence in diagramData
            self.diagramData[i] = seqData.logMapSeq[self.seqLength-1]

    def plot(self):
        plt.scatter(self.mu, self.diagramData, s=5, marker="o")
        plt.xlabel("mu")
        plt.ylabel("asymptote")
        plt.show()


# =============================================================================


def exercise1aFixedPoint():
    sequence = logMapClass(0.9, 2, 100)
    sequence.plot()


def exercise1aMultipleAttractors():
    sequence = logMapClass(0.9, 3, 100)
    sequence.plot()


def exercise1aChaoticBehavior():
    sequence = logMapClass(0.9, 4, 100)
    sequence.plot()


def exercise1b():
    plotData = bifuricalDiagramPlotData(200, 10000)
    plotData.plot()

# =============================================================================


exercise1b()
