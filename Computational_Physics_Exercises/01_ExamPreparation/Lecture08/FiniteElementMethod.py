import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
import random


class gaussPointsClass:

    eps = 3e-14  # adjust accuracy

    job = ""

    points = np.empty((10, 1))  # gausspo x
    weights = np.empty((10, 1))  # gausspo weight

    def __init__(self, npts, job, a, b):

        self.job = job

        self.weights = np.empty(npts)
        self.points = np.empty(npts)

        m = (npts + 1) / 2

        for i in range(1, int(m + 1)):
            t = np.cos(np.pi * (i - 0.25) / (npts + 0.5))
            t1 = 1
            while abs(t - t1) >= self.eps:
                p1 = 1
                p2 = 0
                for j in range(1, npts + 1):
                    p3 = p2
                    p2 = p1
                    p1 = ((2.0 * j - 1.0) * t * p2 - (j - 1.0) * p3) / j

                pp = npts * (t * p1 - p2) / (t * t - 1.0)
                t1 = t
                t = t1 - p1 / pp

            self.points[i - 1] = -t
            self.points[npts - i] = t
            self.weights[i - 1] = 2.0 / ((1.0 - t * t) * pp * pp)
            self.weights[npts - i] = self.weights[i - 1]

        if job == 0:
            for i in range(0, npts):
                self.points[i] = self.points[i] * (b - a) / 2 + (b + a) / 2
                self.weights[i] = self.weights[i] * (b - a) / 2

        if job == 1:
            for i in range(0, npts):
                xi = self.points[i]
                self.points[i] = a * b * (1 + xi) / (b + a - (b - a) * xi)
                self.weights[i] = (
                    self.weights[i]
                    * 2
                    * a
                    * b
                    * b
                    / ((b + a - (b - a) * xi) * (b + a - (b - a) * xi))
                )

        if job == 2:
            for i in range(0, npts):
                xi = self.points[i]
                self.points[i] = (b * xi + b + a + a) / (1 - xi)
                self.weights[i] = self.weights[i] * 2 * (a + b) / ((1 - xi) * (1 - xi))


def basisFunction(positions, index, position):
    if position >= positions[index - 1] and position <= positions[index]:
        return (position - positions[index - 1]) / (
            positions[index] - positions[index - 1]
        )

    if position >= positions[index] and position <= positions[index + 1]:
        return (positions[index + 1] - position) / (
            positions[index + 1] - positions[index]
        )
    else:
        return 0


def getPositions(Parameters):
    leftIntervalBorder = Parameters.leftIntervalBorder
    rightIntervalBorder = Parameters.rightIntervalBorder
    elementCount = Parameters.elementCount
    elementDistribution = Parameters.elementDistribution

    if elementDistribution == "random":
        randomPositions = np.empty(elementCount + 1)
        randomPositions[0] = leftIntervalBorder
        randomPositions[elementCount] = rightIntervalBorder
        for index in range(1, elementCount):
            randomPositions[index] = random.uniform(
                leftIntervalBorder, rightIntervalBorder
            )
        randomSortedPositions = np.sort(randomPositions)
        return randomSortedPositions

    if elementDistribution == "equidistant":
        equidistantPositions = np.linspace(
            leftIntervalBorder, rightIntervalBorder, elementCount + 1
        )
        return equidistantPositions


def getElementLengths(positions):
    elementLengths = np.empty(len(positions) - 1)
    for index in range(0, len(elementLengths)):
        elementLengths[index] = positions[index + 1] - positions[index]

    return elementLengths


def getStiffnessMatrix(positions):
    stiffnessMatrix = np.empty((len(positions) - 2, len(positions) - 2))
    for verticalIndex in range(0, len(stiffnessMatrix)):
        for horizontalIndex in range(0, len(stiffnessMatrix)):
            stiffnessMatrix[verticalIndex, horizontalIndex] = getStiffnessMatrixElement(
                verticalIndex, horizontalIndex, positions
            )

    return stiffnessMatrix


def getStiffnessMatrixElement(verticalIndex, horizontalIndex, positions):
    elementLengths = getElementLengths(positions)

    if verticalIndex == horizontalIndex:
        element = (
            1 / elementLengths[verticalIndex] + 1 / elementLengths[verticalIndex + 1]
        )
        return element

    if verticalIndex == horizontalIndex + 1:
        element = -1 / elementLengths[verticalIndex]
        return element

    if horizontalIndex == verticalIndex + 1:
        element = -1 / elementLengths[horizontalIndex]
        return element

    else:
        return 0


def getLoadVector(Parameters, positions):
    loadVector = np.empty(len(positions) - 2)
    for index in range(0, len(loadVector)):
        loadVector[index] = getLoadVectorElement(Parameters, index, positions)

    return np.transpose(loadVector)


def getLoadVectorElement(Parameters, index, positions):
    gauss = gaussPointsClass(32, 0, positions[index], positions[index + 2])
    element = 0
    for gaussPointIndex in range(0, len(gauss.points)):
        element = (
            element
            + integrand(index, positions, gauss.points[gaussPointIndex])
            * gauss.weights[gaussPointIndex]
        )

    element = element + getLoadVectorBoundaryCondition(Parameters, index, positions)

    return element


def getLoadVectorBoundaryCondition(Parameters, index, positions):
    elementLengths = getElementLengths(positions)
    potentialLeftBorder = Parameters.potentialLeftBorder
    potentialRightBorder = Parameters.potentialRightBorder
    if index == 0:
        return 1 / elementLengths[index] * potentialLeftBorder
    if index == len(positions) - 3:
        # loadVector is 2 smaller than positions, get last index of loadVector
        return 1 / elementLengths[index] * potentialRightBorder
    else:
        return 0


def integrand(index, positions, position):
    integrand = (
        4 * np.pi * chargeDensity(position) * basisFunction(positions, index, position)
    )
    return integrand


def getBasisFunctionCoefficients(Parameters, positions):
    stiffnessMatrix = getStiffnessMatrix(positions)
    loadVector = getLoadVector(Parameters, positions)
    basisFunctionCoefficients = LA.inv(stiffnessMatrix).dot(loadVector)
    return basisFunctionCoefficients


def getPotential(Parameters, basisFunctionCoefficients, positions, position):
    potential = 0
    for index in range(0, len(basisFunctionCoefficients)):
        term = basisFunctionCoefficients[index] * basisFunction(
            positions, index, position
        )
        potential = potential + term
    # Boundary conditions
    potential = potential + Parameters.potentialLeftBorder * basisFunction(
        positions, 0, position
    )
    potential = potential + Parameters.potentialRightBorder * basisFunction(
        positions, len(basisFunctionCoefficients), position
    )
    return potential


def plotPotential(Parameters, basisFunctionCoefficients, positions):
    plotPositions = np.linspace(
        Parameters.leftIntervalBorder, Parameters.rightIntervalBorder, 500
    )
    potential = np.empty(len(plotPositions))
    for index in range(0, len(plotPositions)):
        plotPosition = plotPositions[index]
        potential[index] = getPotential(
            Parameters, basisFunctionCoefficients, positions, plotPosition
        )
    plt.plot(plotPositions, potential)
    plt.show()


# ============================================================================


class Parameters:
    elementCount = 128
    leftIntervalBorder = 0
    rightIntervalBorder = 1
    elementDistribution = "equidistant"
    potentialLeftBorder = 0
    potentialRightBorder = 1


def chargeDensity(position):
    return 1 / 4 / np.pi * np.sin(position)


positions = getPositions(Parameters)
plt.plot(positions)
plt.show()

loadVector = getLoadVector(Parameters, positions)
plt.plot(loadVector)
plt.show()

stiffnessMatrix = getStiffnessMatrix(positions)
plt.imshow(stiffnessMatrix)
plt.show()

basisFunctionCoefficients = getBasisFunctionCoefficients(Parameters, positions)
plt.plot(basisFunctionCoefficients)
plt.show()

plotPotential(Parameters, basisFunctionCoefficients, positions)
