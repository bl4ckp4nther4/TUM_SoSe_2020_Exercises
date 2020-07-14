import numpy as np
import matplotlib.pyplot as plt
import random
import sys


def setBar():
    toolbar_width = 100

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['


def updateBar(progress, lastUpdate):
    progress = progress * 100

    delta = int(np.floor(progress) - lastUpdate)
    for i in range(0, delta):
        sys.stdout.write("-")
        sys.stdout.flush()
    return np.floor(progress)


class neuralNetwork:

    eta = 0.01
    h = 0.01

    neurons = 4

    w1 = np.empty(neurons)
    w2 = np.empty(neurons)
    wo = np.empty(neurons)
    b = np.empty(neurons)

    trainingData = [[], [], []]

    def __init__(self, neurons, trainingDataSize):
        self.neurons = neurons
        self.w1 = np.empty(self.neurons)
        self.w2 = np.empty(self.neurons)
        self.wo = np.empty(self.neurons)
        self.b = np.empty(self.neurons)

        self.initState()
        self.initTrainingData(trainingDataSize)

    def initState(self):
        for i in range(0, self.neurons):
            self.w1[i] = random.uniform(1, -1)
            self.w2[i] = random.uniform(1, -1)
            self.wo[i] = random.uniform(1, -1)
            self.b[i] = random.uniform(1, -1)

    def initTrainingData(self, size):
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

    def plotTrainingData(self):
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

    def activationFunc(self, w1, w2, b, x, y):
        # print(w1 * x + w2 * y - b)
        return w1 * x + w2 * y - b

    def output(self, wo, w1, w2, b, x, y):

        if x.size > 1:
            sum = np.zeros((len(x), len(y)))
            term = np.zeros((len(x), len(y)))
            for j in range(0, self.neurons):

                for k in range(0, len(x)):
                    for l in range(0, len(y)):
                        if (
                            np.max(
                                self.activationFunc(
                                    w1[j], w2[j], b[j], x[k, l], y[k, l]
                                )
                            )
                            >= 460
                        ):
                            term[k, l] = 0
                        else:
                            term[k, l] = wo[j] / (
                                1
                                + np.exp(
                                    self.activationFunc(
                                        w1[j], w2[j], b[j], x[k, l], y[k, l]
                                    )
                                )
                            )

                sum = sum + term
        else:
            sum = 0
            term = 0
            for j in range(0, self.neurons):

                if np.max(self.activationFunc(w1[j], w2[j], b[j], x, y)) >= 460:
                    term = 0
                else:
                    term = wo[j] / (
                        1 + np.exp(self.activationFunc(w1[j], w2[j], b[j], x, y))
                    )

                sum = sum + term
        return sum

    def plotOutput(self, border):
        xlist = np.linspace(-border, border, 100)
        ylist = np.linspace(-border, border, 100)
        x, y = np.meshgrid(xlist, ylist)
        z = self.output(self.wo, self.w1, self.w2, self.b, x, y)
        fig, ax = plt.subplots(1, 1)
        cp = ax.contourf(x, y, z)
        ax.set_title("Output")

    def lossFunc(self, wo, w1, w2, b):
        xtemp = self.trainingData[0][0]
        ytemp = self.trainingData[1][0]
        sign = self.trainingData[2][0]

        size = len(sign)

        sum = 0
        for i in range(0, size):
            term = (sign[i] - self.output(wo, w1, w2, b, xtemp[i], ytemp[i])) ** 2
            sum = sum + term

        return sum

    def update(self):
        def dloss_dwo(j):
            h_vec = np.zeros(self.neurons)
            h_vec[j] = self.h
            return (
                self.lossFunc(self.wo + h_vec, self.w1, self.w2, self.b)
                - self.lossFunc(self.wo - h_vec, self.w1, self.w2, self.b)
            ) / (2 * self.h)

        def dloss_dw1(j):
            h_vec = np.zeros(self.neurons)
            h_vec[j] = self.h
            return (
                self.lossFunc(self.wo, self.w1 + h_vec, self.w2, self.b)
                - self.lossFunc(self.wo, self.w1 - h_vec, self.w2, self.b)
            ) / (2 * self.h)

        def dloss_dw2(j):
            h_vec = np.zeros(self.neurons)
            h_vec[j] = self.h
            return (
                self.lossFunc(self.wo, self.w1, self.w2 + h_vec, self.b)
                - self.lossFunc(self.wo, self.w1, self.w2 - h_vec, self.b)
            ) / (2 * self.h)

        def dloss_db(j):
            h_vec = np.zeros(self.neurons)
            h_vec[j] = self.h
            return (
                self.lossFunc(self.wo, self.w1, self.w2, self.b + h_vec)
                - self.lossFunc(self.wo, self.w1, self.w2, self.b - h_vec)
            ) / (2 * self.h)

        for j in range(0, self.neurons):
            if random.random() <= 0.2:
                self.wo[j] = self.wo[j] - self.eta * dloss_dwo(j)
            if random.random() <= 0.2:
                self.w1[j] = self.w1[j] - self.eta * dloss_dw1(j)
            if random.random() <= 0.2:
                self.w2[j] = self.w2[j] - self.eta * dloss_dw2(j)
            if random.random() <= 0.2:
                self.b[j] = self.b[j] - self.eta * dloss_db(j)

    def training(self, iterations):
        cost = np.empty(iterations)
        setBar()
        lastUpdate = 0
        for k in range(0, iterations):
            self.update()
            cost[k] = self.lossFunc(self.wo, self.w1, self.w2, self.b)
            # update progress bar
            lastUpdate = updateBar((k + 1) / iterations, lastUpdate)
            if k % 20 == 0:
                self.plotOutput(1)
                plt.show()

        plt.plot(cost)
        # end progress bar
        sys.stdout.write("]\n")


AI = neuralNetwork(4, 400)

AI.plotOutput(1)
AI.plotTrainingData()
plt.show()

AI.training(800)

AI.plotOutput(1)
AI.plotTrainingData()
plt.show()

# AA.training(100)

