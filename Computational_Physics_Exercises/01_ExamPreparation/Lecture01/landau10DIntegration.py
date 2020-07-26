import numpy as np
import random
import matplotlib.pyplot as plt


def function(x):
    sumSquared = sum(x) ** 2
    return sumSquared


def integralSumSquaredFunction(N):
    sum = 0
    for _ in range(0, N):
        x = generateRandomX(10)
        term = function(x)
        sum = sum + term
    integral = sum / N

    return integral


def generateRandomX(N):
    randomX = np.zeros(N)
    for index in range(0, N):
        randomX[index] = random.random()
    return randomX


sampleSize = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]

integral = np.zeros(len(sampleSize))

for index in range(0, len(sampleSize)):
    N = sampleSize[index]
    integral[index] = integralSumSquaredFunction(N)

integralError = np.absolute(integral - 155 / 6)

plt.plot(1 / np.sqrt(sampleSize), integralError)
plt.show()
