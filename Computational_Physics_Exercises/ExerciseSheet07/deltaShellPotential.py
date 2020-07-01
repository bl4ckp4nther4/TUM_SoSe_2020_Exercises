import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from scipy.optimize import root


class gaussPoints:

    eps = 3e-14  # adjust accuracy

    job = ""
    x = np.empty((10, 1))  # gausspo x
    w = np.empty((10, 1))  # gausspo weight

    def __init__(self, npts, job, a, b):

        self.job = job

        self.w = np.empty((npts, 1))
        self.x = np.empty((npts, 1))

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
            # prf("x[i-1] = %f, w = %f ", x[i - 1], w[npts - i])

        # prf("\n")

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


def createHmatrix(N, k, w, mu, lambd, b):
    H = np.empty((N, N))

    # create the matrix
    for i in range(0, N):
        for j in range(0, N):
            if i == j:
                H[i, j] = (
                    k[i] ** 2 / (2 * mu)
                    + lambd
                    / (np.pi * mu)
                    * np.sin(k[i] * b)
                    / k[i]
                    * np.sin(k[j] * b)
                    * k[j]
                    * w[j]
                )
            else:
                H[i, j] = (
                    lambd
                    / (np.pi * mu)
                    * np.sin(k[i] * b)
                    / k[i]
                    * np.sin(k[j] * b)
                    * k[j]
                    * w[j]
                )  #
    return H


# constants dictated by the exercise sheet
lambd = -10
mu = 1 / 2
b = 5

# vary these parameters to check whether solution converges
N = 1000
k_max = 10000

E_bound = []

for i in range(1, 4):
    N = 10 ** i

    gaussPointsIntegration = gaussPoints(N, 0, 0, k_max)
    k = gaussPointsIntegration.x
    w = gaussPointsIntegration.w

    # create matrix:
    H = createHmatrix(N, k, w, mu, lambd, b)

    # calculate the eigenvalues
    E, Psi = LA.eig(H)

    plt.plot(E)
    plt.show()
    plt.imshow(H)
    plt.show()
    E_min = np.amin(E)

    E_bound = np.append(E_bound, E_min)


plt.plot(E_bound)
plt.show


# solve transcendental equation


def transcendental(kappa, b, lambd):
    return np.exp(-2 * kappa * b) - 1 - 2 * kappa / lambd


kappa = root(transcendental, 5, args=(b, lambd)).x[0]

print(kappa)

E_0 = -(kappa ** 2) / 2 / mu

print(E_0)
