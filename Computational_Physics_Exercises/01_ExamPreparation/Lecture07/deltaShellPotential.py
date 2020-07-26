import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from scipy.optimize import root


class gaussPoints:

    eps = 3e-14  # adjust accuracy

    job = ""
    points = np.empty((10, 1))  # gausspo x
    weights = np.empty((10, 1))  # gausspo weight

    def __init__(self, npts, job, a, b):

        self.job = job

        self.weights = np.empty((npts, 1))
        self.points = np.empty((npts, 1))

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
            # prf("x[i-1] = %f, w = %f ", x[i - 1], w[npts - i])

        # prf("\n")

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


def calculateHamiltonMatrix(Parameters):
    pointCount = Parameters.pointCount

    hamiltonMatrix = np.empty((pointCount, pointCount))
    momentumsAndWeights = gaussPoints(pointCount, 0, 0, Parameters.maxMomentum)
    momentums = momentumsAndWeights.points
    weights = momentumsAndWeights.weights

    for indexVertical in range(0, pointCount):
        for indexHorizontal in range(0, pointCount):
            leftMomentum = momentums[indexVertical]
            rightMomentum = momentums[indexHorizontal]
            potential = calculatePotentialInMomentumSpace(
                Parameters, leftMomentum, rightMomentum
            )

            leftTerm = (
                kroneckerDelta(indexVertical, indexHorizontal)
                * leftMomentum ** 2
                / 2
                / Parameters.mu
            )
            rightTerm = 2 / np.pi * potential * rightMomentum * weights[indexVertical]
            hamiltonMatrix[indexVertical, indexHorizontal] = leftTerm + rightTerm

    return hamiltonMatrix


def calculatePotentialInMomentumSpace(Parameters, momentum, momentumDash):
    potential = (
        Parameters.lambd
        * Parameters.b ** 2
        / 2
        / Parameters.mu
        * besselFunction(momentumDash * Parameters.b)
        * besselFunction(momentum * Parameters.b)
    )
    return potential


def besselFunction(z):
    return np.sin(z) / z


def kroneckerDelta(index1, index2):
    if index1 == index2:
        return 1
    else:
        return 0


def getBoundStateEnergy(hamiltonMatrix):
    allEigenEnergies, _ = LA.eig(hamiltonMatrix)
    if checkOnlySingleBoundState(hamiltonMatrix) == True:
        print("One bound state energy found:", min(allEigenEnergies))
        return min(allEigenEnergies)
    else:
        print("There is not only one bound state energy")
        return False


def getBoundStateWaveFunction(hamiltonMatrix):
    allEigenEnergies, waveFunctions = LA.eig(hamiltonMatrix)
    boundStateEnergy = getBoundStateEnergy(hamiltonMatrix)
    boundStateIndex = list(allEigenEnergies).index(boundStateEnergy)
    boundStateWaveFunction = waveFunctions[:, boundStateIndex]
    return boundStateWaveFunction


def checkOnlySingleBoundState(hamiltonMatrix):
    allEigenEnergies, _ = LA.eig(hamiltonMatrix)
    negativeEnergies = allEigenEnergies[allEigenEnergies < 0]
    if len(negativeEnergies) == 1:
        return True
    else:
        return False


def plotAccuracyOfSolutions(hamiltonMatrix):
    eigenEnergy = getBoundStateEnergy(hamiltonMatrix)
    waveFunction = getBoundStateWaveFunction(hamiltonMatrix)
    leftHandSideVector = np.matmul(waveFunction, np.transpose(hamiltonMatrix))
    rightHandSideVector = eigenEnergy * waveFunction

    plt.plot(leftHandSideVector)
    plt.plot(rightHandSideVector)
    plt.show()

    plt.plot(np.absolute(leftHandSideVector - rightHandSideVector))
    plt.show()


class Parameters:
    pointCount = 128
    maxMomentum = 10

    lambd = -50
    mu = 0.5
    b = 10


hamiltonMatrix = calculateHamiltonMatrix(Parameters)

energy = getBoundStateEnergy(hamiltonMatrix)
waveFunction = getBoundStateWaveFunction(hamiltonMatrix)


plotAccuracyOfSolutions(hamiltonMatrix)

