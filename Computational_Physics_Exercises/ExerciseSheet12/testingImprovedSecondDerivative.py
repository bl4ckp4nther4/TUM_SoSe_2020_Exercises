import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys
import random


def calculateFirstDerivative(function, a):
    length = len(function)
    firstDerivative = np.zeros(length)
    for index in range(0, length):
        indexPlus = (index + 1) % length
        firstDerivative[index] = (function[indexPlus] - function[index]) / a

    return firstDerivative


def calculateSecondDerivative(function, a):
    length = len(function)
    secondDerivative = np.zeros(length)
    for index in range(0, length):
        indexPlus = (index + 1) % length
        indexMinus = (index - 1) % length
        secondDerivative[index] = (
            function[indexPlus] + function[indexMinus] - 2 * function[index]
        ) / a ** 2

    return secondDerivative


def calculateForthDerivative(function, a):
    secondDerivative = calculateSecondDerivative(function, a)
    forthDerivative = calculateSecondDerivative(secondDerivative, a)
    return forthDerivative


def calculateBetterSecondDerivative(function, a):
    betterSecondDerivative = calculateSecondDerivative(
        function, a
    ) - a ** 2 / 12 * calculateForthDerivative(function, a)
    return betterSecondDerivative


pointCount = 200

x = np.linspace(0, 2 * np.pi * (1 - 1 / pointCount), pointCount)
a = 2 * np.pi / 200

function = np.sin(x)

firstDerivativeSquared = calculateFirstDerivative(function, a) ** 2
usingSecondDerivative = -function * calculateBetterSecondDerivative(function, a)

plt.plot(x, firstDerivativeSquared)
plt.plot(x, usingSecondDerivative)
plt.show()

