import numpy as np
import importlib
from numpy import linalg as LA
import matplotlib.pyplot as plt
import random


class gaussPointsClass:

    eps = 3e-14  # adjust accuracy

    job = ""

    x = np.empty((10, 1))  # gausspo x
    w = np.empty((10, 1))  # gausspo weight

    def __init__(self, npts, job, a, b):

        self.job = job

        self.w = np.empty(npts)
        self.x = np.empty(npts)

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

            self.x[i - 1] = -t
            self.x[npts - i] = t
            self.w[i - 1] = 2.0 / ((1.0 - t * t) * pp * pp)
            self.w[npts - i] = self.w[i - 1]

        if job == 0:
            for i in range(0, npts):
                self.x[i] = self.x[i] * (b - a) / 2 + (b + a) / 2
                self.w[i] = self.w[i] * (b - a) / 2

        if job == 1:
            for i in range(0, npts):
                xi = self.x[i]
                self.x[i] = a * b * (1 + xi) / (b + a - (b - a) * xi)
                self.w[i] = (
                    self.w[i]
                    * 2
                    * a
                    * b
                    * b
                    / ((b + a - (b - a) * xi) * (b + a - (b - a) * xi))
                )

        if job == 2:
            for i in range(0, npts):
                xi = self.x[i]
                self.x[i] = (b * xi + b + a + a) / (1 - xi)
                self.w[i] = self.w[i] * 2 * (a + b) / ((1 - xi) * (1 - xi))


def randxVector(a, b, npts):
    randVector = np.empty(npts)
    for i in range(0, npts):
        randVector[i] = random.uniform(a, b)

    randxVector = np.sort(randVector)
    return randxVector


def alpha_numerical(a, b, N, U_a, U_b, xVector):

    # define h
    h = np.empty(N)
    for i in range(0, N):
        h[i] = xVector[i + 1] - xVector[i]

    def rho(x):
        return 1 / 4 / np.pi

    def phi(i, x, xVector, h):
        if x < xVector[i - 1] or x > xVector[i + 1]:
            return 0
        if x >= xVector[i - 1] and x <= xVector[i]:
            return (x - xVector[i - 1]) / h[i - 1]
        if x >= xVector[i] and x <= xVector[i + 1]:
            return (xVector[i + 1] - x) / h[i]

    # ================================================================
    # CALCULATE b:
    bVector = np.empty(N - 1)
    npts = 100  # number of points for the guass integration
    for i in range(1, N):
        # set up the integrand
        def integrand(x):
            return 4 * np.pi * rho(x) * phi(i, x, xVector, h)

        quadra = 0
        gaussPoints = gaussPointsClass(npts, 0, a, b)  # return gauss points and weights
        for n in range(0, npts):  # calculate integral
            quadra = quadra + integrand(gaussPoints.x[n]) * gaussPoints.w[n]

        bVector[
            i - 1
        ] = quadra  # calculate the elenetns of the b vector (b-1 because we start at i = 1 and end at i = N)

    # =======================================================================================
    # calculate ATilde:
    ATilde0 = np.empty(N - 1)
    for i in range(1, N):
        if i == 1:
            ATilde0[i - 1] = -1 / h[0]
        else:
            ATilde0[i - 1] = 0

    ATildeN = np.empty(N - 1)
    for i in range(1, N):
        if i == N - 1:
            ATildeN[i - 1] = -1 / h[N - 1]
        else:
            ATildeN[i - 1] = 0

    # calculate bDash:
    bDash = np.empty(N - 1)
    for i in range(1, N):
        bDash[i - 1] = bVector[i - 1] - ATilde0[i - 1] * U_a - ATildeN[i - 1] * U_b

    # =======================================================================================
    # callculate AMatrix
    AMatrix = np.empty((N - 1, N - 1))
    for i in range(1, N):
        for j in range(1, N):

            if i == j:
                AMatrix[i - 1, j - 1] = 1 / h[i - 1] + 1 / h[i]

            elif i - j == 1:
                AMatrix[i - 1, j - 1] = -1 / h[j]

            elif i - j == -1:
                AMatrix[i - 1, j - 1] = -1 / h[i]

            else:
                AMatrix[i - 1, j - 1] = 0

    # =======================================================================================
    # calcuöate the alpha vector
    alpha = LA.inv(AMatrix).dot(bDash)
    return alpha


def U_numerical(x, a, b, N, U_a, U_b, xVector, alpha):

    # define h
    h = np.empty(N)
    for i in range(0, N):
        h[i] = xVector[i + 1] - xVector[i]

    # define phi
    def phi(i, x, xVector, h):
        if x >= xVector[i - 1] and x <= xVector[i]:
            return (x - xVector[i - 1]) / h[i - 1]
        if x >= xVector[i] and x <= xVector[i + 1]:
            return (xVector[i + 1] - x) / h[i]
        if x < xVector[i - 1] or x > xVector[i + 1]:
            return 0

    # calculate U
    sum = 0
    for j in range(1, N):
        sum = sum + alpha[j - 1] * phi(j, x, xVector, h)

    U = sum + U_a * phi(0, x, xVector, h) + U_b * phi(N, x, xVector, h)
    return U


def U_analytical(x):
    return -x * (x - 3) / 2


U_a = 0
U_b = 1

a = 0
b = 1


# number of elements
for N in range(3, 101):

    # define the nodes of the elements
    xVector = randxVector(a, b, N + 1)

    numericalFullRange = np.empty(101)
    analyticalFullRange = np.empty(101)
    x = np.linspace(a, b, 101)
    alpha = alpha_numerical(a, b, N, U_a, U_b, xVector)
    for k in range(0, 101):
        if k % 10 == 0:
            print(k)
        numericalFullRange[k] = U_numerical(x[k], a, b, N, U_a, U_b, xVector, alpha)
        analyticalFullRange[k] = U_analytical(x[k])
    plt.plot(numericalFullRange)
    plt.plot(analyticalFullRange)
    plt.show()

    # calculate accuracy of the numerical solution:
    meanSquareError[N] = sum((numericalFullRange - analyticalFullRange) ** 2)
    print(N)


plt.plot(meanSquareError)
plt.show

