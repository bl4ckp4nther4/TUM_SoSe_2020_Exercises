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

    learningRate = 0.01
    deltaWeightsAndBiases = 0.01

    neuronCount = 4

    weightsInput1 = np.empty(neuronCount)
    weightsInput2 = np.empty(neuronCount)
    weightsOutput = np.empty(neuronCount)
    biases = np.empty(neuronCount)

    trainingData = [[], [], []]

    def __init__(self, neurons, trainingDataSize):
        self.neuronCount = neurons
        self.weightsInput1 = np.empty(self.neuronCount)
        self.weightsInput2 = np.empty(self.neuronCount)
        self.weightsOutput = np.empty(self.neuronCount)
        self.biases = np.empty(self.neuronCount)

        self.initializeState()
        self.initializeTrainingData(trainingDataSize)

    def initializeState(self):
        for i in range(0, self.neuronCount):
            self.weightsInput1[i] = random.uniform(1, -1)
            self.weightsInput2[i] = random.uniform(1, -1)
            self.weightsOutput[i] = random.uniform(1, -1)
            self.biases[i] = random.uniform(1, -1)

    def initializeTrainingData(self, trainingDataSize):
        trainingDataX = np.empty(trainingDataSize)
        trainingDataY = np.empty(trainingDataSize)
        traingingDataSign = np.empty(trainingDataSize)

        for trainingDataIndex in range(0, trainingDataSize):
            trainingDataX[trainingDataIndex] = random.uniform(1, -1)
            trainingDataY[trainingDataIndex] = random.uniform(1, -1)
            traingingDataSign[trainingDataIndex] = np.sign(
                trainingDataX[trainingDataIndex] * trainingDataY[trainingDataIndex]
            )

        self.trainingData[0] = [trainingDataX]
        self.trainingData[1] = [trainingDataY]
        self.trainingData[2] = [traingingDataSign]

    def plotTrainingData(self):
        trainingDataX = self.trainingData[0][0]
        trainingDataY = self.trainingData[1][0]
        trainingDataSign = self.trainingData[2][0]

        trainingDataLength = len(trainingDataSign)

        positiveQuadrantX = np.empty(trainingDataLength)
        positiveQuadrantY = np.empty(trainingDataLength)
        negativeQuadrantX = np.empty(trainingDataLength)
        negativeQuadrantY = np.empty(trainingDataLength)
        positiveQuadrantX[:] = np.NaN
        positiveQuadrantY[:] = np.NaN
        negativeQuadrantX[:] = np.NaN
        negativeQuadrantY[:] = np.NaN
        for i in range(0, trainingDataLength):
            if trainingDataSign[i] == 1:
                positiveQuadrantX[i] = trainingDataX[i]
                positiveQuadrantY[i] = trainingDataY[i]
            elif trainingDataSign[i] == -1:
                negativeQuadrantX[i] = trainingDataX[i]
                negativeQuadrantY[i] = trainingDataY[i]

        plt.scatter(positiveQuadrantX, positiveQuadrantY, color="red")
        plt.scatter(negativeQuadrantX, negativeQuadrantY)

    def activationFunction(self, weightInput1, weightInput2, bias, x, y):
        return weightInput1 * x + weightInput2 * y - bias

    def exponentialOverflow(self, exponent):
        if np.max(exponent) >= 460:
            return True
        else:
            return False

    def output(self, weightsOutput, weightsInput1, weightsInput2, biases, x, y):

        if x.size == 1:
            outputSum = 0
            outputTerm = 0
            for neuronIndex in range(0, self.neuronCount):
                thisNeuronsActivationFunction = self.activationFunction(
                    weightsInput1[neuronIndex],
                    weightsInput2[neuronIndex],
                    biases[neuronIndex],
                    x,
                    y,
                )
                if self.exponentialOverflow(thisNeuronsActivationFunction) == True:
                    outputTerm = 0
                else:
                    outputTerm = weightsOutput[neuronIndex] / (
                        1 + np.exp(thisNeuronsActivationFunction)
                    )
                outputSum = outputSum + outputTerm
        elif x.size > 1:
            outputSum = np.zeros((len(x), len(y)))
            outputTerm = np.zeros((len(x), len(y)))
            for neuronIndex in range(0, self.neuronCount):
                for k in range(0, len(x)):
                    for l in range(0, len(y)):
                        thisNeuronsActivationFunction = self.activationFunction(
                            weightsInput1[neuronIndex],
                            weightsInput2[neuronIndex],
                            biases[neuronIndex],
                            x[k, l],
                            y[k, l],
                        )
                        if (
                            self.exponentialOverflow(thisNeuronsActivationFunction)
                            == True
                        ):
                            outputTerm[k, l] = 0
                        else:
                            outputTerm[k, l] = weightsOutput[neuronIndex] / (
                                1 + np.exp(thisNeuronsActivationFunction)
                            )
                outputSum = outputSum + outputTerm

        return outputSum

    def plotOutput(self):
        border = 1
        xlist = np.linspace(-border, border, 100)
        ylist = np.linspace(-border, border, 100)
        x, y = np.meshgrid(xlist, ylist)
        z = self.output(
            self.weightsOutput,
            self.weightsInput1,
            self.weightsInput2,
            self.biases,
            x,
            y,
        )
        fig, ax = plt.subplots(1, 1)
        cp = ax.contourf(x, y, z)
        ax.set_title("Output")

    def lossFunction(self, wo, weightsInput1, weightsInput2, b):
        xtemp = self.trainingData[0][0]
        ytemp = self.trainingData[1][0]
        sign = self.trainingData[2][0]

        size = len(sign)

        sum = 0
        for i in range(0, size):
            term = (
                sign[i]
                - self.output(wo, weightsInput1, weightsInput2, b, xtemp[i], ytemp[i])
            ) ** 2
            sum = sum + term

        return sum

    def update(self):
        def dloss_dweightOutput(neuronIndex):
            deltaVector = np.zeros(self.neuronCount)
            deltaVector[neuronIndex] = self.deltaWeightsAndBiases
            return (
                self.lossFunction(
                    self.weightsOutput + deltaVector,
                    self.weightsInput1,
                    self.weightsInput2,
                    self.biases,
                )
                - self.lossFunction(
                    self.weightsOutput - deltaVector,
                    self.weightsInput1,
                    self.weightsInput2,
                    self.biases,
                )
            ) / (2 * self.deltaWeightsAndBiases)

        def dloss_dweightInput1(neuronIndex):
            deltaVector = np.zeros(self.neuronCount)
            deltaVector[neuronIndex] = self.deltaWeightsAndBiases
            return (
                self.lossFunction(
                    self.weightsOutput,
                    self.weightsInput1 + deltaVector,
                    self.weightsInput2,
                    self.biases,
                )
                - self.lossFunction(
                    self.weightsOutput,
                    self.weightsInput1 - deltaVector,
                    self.weightsInput2,
                    self.biases,
                )
            ) / (2 * self.deltaWeightsAndBiases)

        def dloss_dweightInput2(neuronIndex):
            deltaVector = np.zeros(self.neuronCount)
            deltaVector[neuronIndex] = self.deltaWeightsAndBiases
            return (
                self.lossFunction(
                    self.weightsOutput,
                    self.weightsInput1,
                    self.weightsInput2 + deltaVector,
                    self.biases,
                )
                - self.lossFunction(
                    self.weightsOutput,
                    self.weightsInput1,
                    self.weightsInput2 - deltaVector,
                    self.biases,
                )
            ) / (2 * self.deltaWeightsAndBiases)

        def dloss_dbias(neuronIndex):
            deltaVector = np.zeros(self.neuronCount)
            deltaVector[neuronIndex] = self.deltaWeightsAndBiases
            return (
                self.lossFunction(
                    self.weightsOutput,
                    self.weightsInput1,
                    self.weightsInput2,
                    self.biases + deltaVector,
                )
                - self.lossFunction(
                    self.weightsOutput,
                    self.weightsInput1,
                    self.weightsInput2,
                    self.biases - deltaVector,
                )
            ) / (2 * self.deltaWeightsAndBiases)

        def updateComponent(component, neuronIndex):
            if component == "outputWeight":
                self.weightsOutput[neuronIndex] = self.weightsOutput[
                    neuronIndex
                ] - self.learningRate * dloss_dweightOutput(neuronIndex)
            if component == "input1Weight":
                self.weightsInput1[neuronIndex] = self.weightsInput1[
                    neuronIndex
                ] - self.learningRate * dloss_dweightInput1(neuronIndex)
            if component == "input2Weight":
                self.weightsInput2[neuronIndex] = self.weightsInput2[
                    neuronIndex
                ] - self.learningRate * dloss_dweightInput2(neuronIndex)
            if component == "bias":
                self.biases[neuronIndex] = self.biases[
                    neuronIndex
                ] - self.learningRate * dloss_dbias(neuronIndex)

        for neuronIndex in range(0, self.neuronCount):
            if random.random() <= 0.2:
                updateComponent("outputWeight", neuronIndex)
            if random.random() <= 0.2:
                updateComponent("input1Weight", neuronIndex)
            if random.random() <= 0.2:
                updateComponent("input2Weight", neuronIndex)
            if random.random() <= 0.2:
                updateComponent("bias", neuronIndex)

    def training(self, trainingIterations, plot=False):
        cost = np.empty(trainingIterations)
        setBar()
        lastUpdate = 0
        for trainingsIteration in range(0, trainingIterations):
            self.update()
            cost[trainingsIteration] = self.lossFunction(
                self.weightsOutput, self.weightsInput1, self.weightsInput2, self.biases
            )
            # update progress bar
            lastUpdate = updateBar(
                (trainingsIteration + 1) / trainingIterations, lastUpdate
            )
            if plot == True and trainingsIteration % 20 == 0:
                self.plotOutput()
                plt.show()

        plt.plot(cost)
        # end progress bar
        sys.stdout.write("]\n")


AI = neuralNetwork(4, 400)

AI.plotOutput()
AI.plotTrainingData()
plt.show()

AI.training(800, plot=True)

AI.plotOutput()
AI.plotTrainingData()
plt.show()

# AA.training(100)

