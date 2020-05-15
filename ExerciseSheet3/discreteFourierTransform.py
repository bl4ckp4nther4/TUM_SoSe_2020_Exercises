import numpy as np
import matplotlib.pyplot as plt

# this program calculates the Fourier transform and inverse Fourier transform of a on dimensional function


class fourierTransParent():
    N = 1  # number of data points
    T = 1  # time period of evaluation
    h = T / N  # distance of data points in time
    t_k = np.zeros(N)  # list of all time steps
    w_n = np.zeros(N)  # list of all frequency steps

    Z = 1
    A_nk = np.zeros((N, N))  # matrix for f transform
    Adash_nk = np.zeros((N, N))  # matrix for inverse f transform

    y_k = np.zeros(N)
    Y_n = np.zeros(N)
    y_k_back = np.zeros(N)

    variance = 0

    def __init__(self, N, T):
        # initialize a discrete representation of the function and its Fourier transform
        self.N = N
        self.T = T
        self.h = T / N
        self.t_k = np.linspace(0, self.T, self.N)
        self.w_n = np.arange(1, N+1, 1) * 2*np.pi / (self.N * self.h)

        self.sety_k()
        self.setY_n()
        self.sety_k_back()
        self.setVariance()

    def y(self, t):
        # function in the time domain
        return t

    def sety_k(self):
        # set the discrete representation of the function
        self.y_k = np.zeros(self.N)
        for k in range(1, self.N+1):
            self.y_k[k-1] = self.y(self.t_k[k-1])

    def setY_n(self):
        # set the discrete representation of the Fourier transform of the function
        self.sety_k()
        self.setA_nk()

        self.Y_n = np.zeros(self.N, dtype=complex)
        for n in range(1, self.N+1):
            # calculate each element of Y_n
            sum = 0
            term = 0

            for k in range(1, self.N+1):
                # calculate the terms for the sum
                term = self.A_nk[n-1][k-1]*self.y_k[k-1]
                sum = sum + term

            # set the Y_n to the sum
            self.Y_n[n-1] = sum

    def sety_k_back(self):
        self.setY_n()
        self.setAdash_nk()

        sum = 0
        term = 0
        self.y_k_back = np.zeros(self.N, dtype=complex)
        for k in range(1, self.N+1):
            # calculate each element of Y_n
            sum = 0
            term = 0

            for n in range(1, self.N+1):
                # calculate the terms for the sum
                term = self.Adash_nk[n-1][k-1]*self.Y_n[n-1]
                sum = sum + term

            # set the Y_n to the sum
            self.y_k_back[k-1] = sum

    def setA_nk(self):
        # set matrix for the multiplication in the sum of the Fourier transform
        self.setZ()
        self.A_nk = np.zeros((self.N, self.N), dtype=complex)

        for n in range(1, self.N+1):
            for k in range(1, self.N+1):
                self.A_nk[n-1, k-1] = 1/np.sqrt(2*np.pi) * self.Z ** (n*k)

    def setAdash_nk(self):
        # set matrix for the multiplication in the sum of the inverse transform
        self.setZ()
        self.Adash_nk = np.zeros((self.N, self.N), dtype=complex)
        for n in range(1, self.N+1):
            for k in range(1, self.N+1):
                self.Adash_nk[n-1, k -
                              1] = np.sqrt(2*np.pi) / self.N * self.Z ** (-n*k)

    def setZ(self):
        # set the Z
        self.Z = np.exp(- 2 * np.pi * 1j / self.N)

    def setVariance(self):
        # calculate the variance of the back transform in relation to y_k
        term = 0
        sum = 0
        for i in range(1, self.N):
            term = (self.y_k_back[i].real - self.y_k[i])**2 / self.N
            sum = sum + term
        self.variance = sum
        if self.variance > 1e-14:
            print("Variance of back transform is high: ", self.variance)

    def ploty_k(self):
        plt.plot(self.t_k, self.y_k)
        plt.ylabel("y_k")
        plt.xlabel("t_k")
        plt.show()

    def ploty_kAndy_k_back(self):
        plt.plot(self.t_k, self.y_k)
        plt.plot(self.t_k, self.y_k_back)
        plt.ylabel("y_k")
        plt.xlabel("t_k")
        plt.show()

    def plotRealAndImag(self):
        plt.plot(self.w_n, self.Y_n.real)
        plt.plot(self.w_n, self.Y_n.imag)
        plt.ylabel("re(Y_n), blue; im(Y_n), orange")
        plt.xlabel("w_n")
        plt.show()

# ====================================

# 1a)


class sawtoothFourier(fourierTransParent):
    def y(self, t):
        if t >= (self.T/2):
            return t
        if t < (self.T/2):
            return t + self.T

# 1b)


class g1(fourierTransParent):
    def y(self, t):
        return np.sin(t)


class g2(fourierTransParent):
    def y(self, t):
        return np.cos(t)


class g3(fourierTransParent):
    def y(self, t):
        return 3 + np.cos(t)


class g4(fourierTransParent):
    def y(self, t):
        return 3 + np.cos(5 + t)


# 1c)
class expon(fourierTransParent):
    def y(self, t):
        return np.exp(-t / (2*np.pi))


# 1d)
class quadratic(fourierTransParent):
    def y(self, t):
        return t**2


class cubic(fourierTransParent):
    def y(self, t):
        return t**3

# ========================================================================================


def exercise1a1():
    sawtooth = sawtoothFourier(128, 1)
    # plot real and imag part of Y_n
    sawtooth.plotRealAndImag()


def exercise1a2():
    sawtooth = sawtoothFourier(128, 1)
    # plot y_k and backtransformation
    sawtooth.ploty_kAndy_k_back()


def exercise1b():
    sinus = g1(8, np.pi*2)
    cosinus1 = g2(8, np.pi*2)
    cosinus2 = g2(8, np.pi*2)
    cosinus3 = g2(8, np.pi*2)

    # plot real and imag part of Y_n
    sinus.plotRealAndImag()
    cosinus1.plotRealAndImag()
    cosinus2.plotRealAndImag()
    cosinus3.plotRealAndImag()


def exercise1c():
    exponential = expon(128, 4)
    # plot the exponential, as well as the rea and imag parts of the transformation
    plt.plot(exponential.y_k)
    plt.show()
    plt.plot(exponential.Y_n.real)
    plt.plot(exponential.Y_n.imag)
    plt.show()


def exercise1dEven():
    even = quadratic(128, 2)
    # plot the even function, as well as the rea and imag parts of the transformation
    even.ploty_k()
    even.plotRealAndImag()


def exercise1dOdd():
    odd = cubic(128, 2)
    # plot the odd function, as well as the rea and imag parts of the transformation
    odd.ploty_k()
    odd.plotRealAndImag()


# ==================================================================================================

exercise1dOdd()
