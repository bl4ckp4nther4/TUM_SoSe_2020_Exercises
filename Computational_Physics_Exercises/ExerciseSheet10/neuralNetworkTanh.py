import numpy as np
import matplotlib.pyplot as plt
import random
import sys
from datetime import datetime


class progressBar:
    toolbarWidth = 100
    lastUpdate = 0

    def __init__(self):
        self.toolbarWidth = 100

        # setup toolbar
        sys.stdout.write("[%s]" % (" " * self.toolbarWidth))
        sys.stdout.flush()
        sys.stdout.write(
            "\b" * (self.toolbarWidth + 1)
        )  # return to start of line, after '['

    def updateBar(self, progress):
        progressBits = progress * self.toolbarWidth

        delta = int(np.floor(progressBits) - self.lastUpdate)
        for i in range(0, delta):
            sys.stdout.write("-")
            sys.stdout.flush()
        self.lastUpdate = np.floor(progressBits)

    def finishBar(self):
        sys.stdout.write("]\n")


def ReLU(x):
    if x >= 0:
        return x
    else:
        return 0


class neuralNetwork:

    dateTimeID = ""

    eta = 0.01
    h = 0.01

    neurons = 4

    wo = np.empty(neurons)
    w1 = np.empty(neurons)
    w2 = np.empty(neurons)
    b = np.empty(neurons)

    trainingData = [[], [], []]

    updateCount = 0
    costAll = []
    woAll = []
    w1All = []
    w2All = []
    bAll = []

    def __init__(self, neurons, trainingDataSize):
        # datetime to identify network
        now = datetime.now()
        self.dateTimeID = now.strftime("%d%m%Y%H%M%S")

        self.neurons = neurons

        self._initState_()
        self._initTrainingData_(trainingDataSize)

    def _initState_(self):
        for i in range(0, self.neurons):
            self.w1[i] = random.uniform(1, -1)
            self.w2[i] = random.uniform(1, -1)
            self.wo[i] = random.uniform(1, -1)
            self.b[i] = random.uniform(1, -1)

        self.woAll = np.append(self.woAll, self.wo)
        self.w1All = np.append(self.w1All, self.w1)
        self.w2All = np.append(self.w2All, self.w2)
        self.bAll = np.append(self.bAll, self.b)

    def _initTrainingData_(self, size):
        xtemp = np.empty(size)
        ytemp = np.empty(size)
        sign = np.empty(size)

        for i in range(0, size):
            xtemp[i] = random.uniform(1, -1)
            ytemp[i] = random.uniform(1, -1)
            sign[i] = np.sign(xtemp[i] * ytemp[i])

        self.trainingData[0] = [xtemp]
        self.trainingData[1] = [ytemp]
        self.trainingData[2] = [sign]

    def _activationFunc_(self, w1, w2, b, x, y):
        # print(w1 * x + w2 * y - b)
        return w1 * x + w2 * y - b

    def _threshold_(self, z):
        return 1 / 2 * np.tanh(z) + 1 / 2

    def _costFunc_(self, wo, w1, w2, b):
        xtemp = self.trainingData[0][0]
        ytemp = self.trainingData[1][0]
        sign = self.trainingData[2][0]

        size = len(sign)

        sum = 0
        for i in range(0, size):
            term = (sign[i] - self.output(wo, w1, w2, b, xtemp[i], ytemp[i])) ** 2
            sum = sum + term

        return sum

    def output(self, wo, w1, w2, b, x, y):

        if x.size > 1:
            sum = np.zeros((len(x), len(y)))
            term = np.zeros((len(x), len(y)))
            # loop through all the neurons
            for j in range(0, self.neurons):

                for k in range(0, len(x)):
                    for l in range(0, len(y)):
                        term = wo[j] * self._threshold_(
                            self._activationFunc_(w1[j], w2[j], b[j], x, y)
                        )

                sum = sum + term
        else:
            sum = 0
            term = 0
            # loop through all the neurons
            for j in range(0, self.neurons):
                term = wo[j] * (
                    1 / 2 * np.tanh(self._activationFunc_(w1[j], w2[j], b[j], x, y))
                    + 1 / 2
                )

                sum = sum + term
        return sum

    def update(self):

        # derivative functions:
        def _dloss_dwo_(j):
            h_vec = np.zeros(self.neurons)
            h_vec[j] = self.h

            return (
                self._costFunc_(self.wo + h_vec, self.w1, self.w2, self.b,)
                - self._costFunc_(self.wo - h_vec, self.w1, self.w2, self.b,)
            ) / (2 * self.h)

        def _dloss_dw1_(j):
            h_vec = np.zeros(self.neurons)
            h_vec[j] = self.h

            return (
                self._costFunc_(self.wo, self.w1 + h_vec, self.w2, self.b,)
                - self._costFunc_(self.wo, self.w1 - h_vec, self.w2, self.b,)
            ) / (2 * self.h)

        def _dloss_dw2_(j):
            h_vec = np.zeros(self.neurons)
            h_vec[j] = self.h

            return (
                self._costFunc_(self.wo, self.w1, self.w2 + h_vec, self.b,)
                - self._costFunc_(self.wo, self.w1, self.w2 - h_vec, self.b,)
            ) / (2 * self.h)

        def _dloss_db_(j):
            h_vec = np.zeros(self.neurons)
            h_vec[j] = self.h

            return (
                self._costFunc_(self.wo, self.w1, self.w2, self.b + h_vec)
                - self._costFunc_(self.wo, self.w1, self.w2, self.b - h_vec)
            ) / (2 * self.h)

        # randomly update a weight or bias
        for j in range(0, self.neurons):
            if random.random() <= 0.2:
                self.wo[j] = self.wo[j] - self.eta * _dloss_dwo_(j)
            if random.random() <= 0.2:
                self.w1[j] = self.w1[j] - self.eta * _dloss_dw1_(j)
            if random.random() <= 0.2:
                self.w2[j] = self.w2[j] - self.eta * _dloss_dw2_(j)
            if random.random() <= 0.2:
                self.b[j] = self.b[j] - self.eta * _dloss_db_(j)

        # update cost and weights, biases
        self.woAll = np.append(self.woAll, self.wo)
        self.w1All = np.append(self.w1All, self.w1)
        self.w2All = np.append(self.w2All, self.w2)
        self.bAll = np.append(self.bAll, self.b)
        self.costAll = np.append(
            self.costAll, self._costFunc_(self.wo, self.w1, self.w2, self.b,),
        )
        self.updateCount = len(self.costAll)

    def training(self, iterations):

        # progress bar
        bar = progressBar()

        oldUpdates = len(self.costAll)

        while self.updateCount <= (oldUpdates + iterations):
            k = self.updateCount - oldUpdates

            # update the weights and biases
            self.update()

            # update progress bar
            bar.updateBar((k + 1) / iterations)

        # end progress bar
        bar.finishBar()

    def plotOutput(self, iteration):
        # indices for the weights and biases
        iteration = int(iteration)
        a = 4 * iteration
        b = 4 * iteration + 4
        # plot output
        border = 1
        xlist = np.linspace(-border, border, 50)
        ylist = np.linspace(-border, border, 50)
        x, y = np.meshgrid(xlist, ylist)
        z = self.output(
            self.woAll[a:b], self.w1All[a:b], self.w2All[a:b], self.bAll[a:b], x, y,
        )
        fig, ax = plt.subplots(1, 1)
        cp = ax.contourf(x, y, z)
        ax.set_title("Output")

        # plot the trainingdata
        xtemp = self.trainingData[0][0]
        ytemp = self.trainingData[1][0]
        sign = self.trainingData[2][0]

        size = len(sign)

        xposq = np.empty(size)
        yposq = np.empty(size)
        xnegq = np.empty(size)
        ynegq = np.empty(size)
        xposq[:] = np.NaN
        yposq[:] = np.NaN
        xnegq[:] = np.NaN
        ynegq[:] = np.NaN
        for i in range(0, size):
            if sign[i] == 1:
                xposq[i] = xtemp[i]
                yposq[i] = ytemp[i]
            elif sign[i] == -1:
                xnegq[i] = xtemp[i]
                ynegq[i] = ytemp[i]

        plt.scatter(xposq, yposq, color="red")
        plt.scatter(xnegq, ynegq)
        plt.show()

    def plotCost(self):
        plt.plot(self.costAll)
        plt.show()

    def saveOutputToFile(self, fileName, iteration):
        # output
        border = 1
        xlist = np.linspace(-border, border, 100)
        ylist = np.linspace(-border, border, 100)
        x, y = np.meshgrid(xlist, ylist)
        z = self.output(
            self.wo[:, iteration],
            self.w1[:, iteration],
            self.w2[:, iteration],
            self.b[:, iteration],
            x,
            y,
        )
        fig, ax = plt.subplots(1, 1)
        cp = ax.contourf(x, y, z)
        ax.set_title("Output")

        # Training Data
        xtemp = self.trainingData[0][0]
        ytemp = self.trainingData[1][0]
        sign = self.trainingData[2][0]

        size = len(sign)

        xposq = np.empty(size)
        yposq = np.empty(size)
        xnegq = np.empty(size)
        ynegq = np.empty(size)
        xposq[:] = np.NaN
        yposq[:] = np.NaN
        xnegq[:] = np.NaN
        ynegq[:] = np.NaN
        for i in range(0, size):
            if sign[i] == 1:
                xposq[i] = xtemp[i]
                yposq[i] = ytemp[i]
            elif sign[i] == -1:
                xnegq[i] = xtemp[i]
                ynegq[i] = ytemp[i]

        plt.scatter(xposq, yposq, color="red")
        plt.scatter(xnegq, ynegq)

        plt.savefig(
            "Computational_Physics_Exercises/ExerciseSheet10/output/"
            + fileName
            + ".png"
        )

    def saveCostToFile(self, fileName):
        plt.plot(self.costAll)
        plt.savefig(fileName)


# ============================================================================0

N = 1000

AI = neuralNetwork(4, 100)
AI.plotOutput(0)
AI.training(N)
AI.plotOutput(N)
AI.plotCost()

AI.plotOutput(100)
AI.plotOutput(200)
AI.plotOutput(300)
AI.plotOutput(400)
AI.plotOutput(500)
AI.plotOutput(600)
AI.plotOutput(700)
AI.plotOutput(800)
AI.plotOutput(900)
AI.plotOutput(1000)
