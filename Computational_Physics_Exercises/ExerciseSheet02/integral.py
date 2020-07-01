import numpy as np
import random
import time

# basic integral class with f(x)= x
class integralParent:

    a = 0  # integral start
    b = 0  # integral end
    N = 0  # numer of points

    # class constructor
    def __init__(self, a, b):
        self.a = a
        self.b = b

    # function that will be integrated
    def integrand(self, x):
        return x

    # analytical antiderivative
    def antiDerivative(self, x):
        return 1 / 2 * x ** 2

    # analytically calculated Integral
    def analyticalInt(self):
        return self.antiDerivative(self.b) - self.antiDerivative(self.a)

    def MCMean(self, N):
        # calculating integral with the Monte Carlo mean method
        x = np.linspace(0, 2, N)
        sum = 0
        term = 0

        # calculating sum
        for i in range(1, N):
            r = random.random()
            x[i] = self.weight(r)
            term = self.integrand(x[i])
            sum = sum + term

        integral = sum / N * (self.b - self.a)
        return integral

    def weight(self, r):
        return r * (self.b - self.a) + self.a

    def MCRejection(self, floor, ceiling, N):
        # calculating function with the Monte Carlo rejection method

        x = np.linspace(0, 2, N)
        y = np.linspace(0, 2, N)
        sum = 0
        term = 0
        N_in = 0

        # find points
        for i in range(1, N):

            x[i] = random.random() * (self.b - self.a) + self.a
            y[i] = random.random() * (ceiling - floor) + floor

            # for f(x) >= 0 and y >= 0
            if self.integrand(x[i]) >= 0 and y[i] >= 0:
                if y[i] <= self.integrand(x[i]):
                    N_in = N_in + 1

            # for f(x) >= 0 and y >= 0
            if self.integrand(x[i]) < 0 and y[i] < 0:
                if y[i] >= self.integrand(x[i]):
                    N_in = N_in + 1

        proportionIn = N_in / N

        integral = proportionIn * (self.b - self.a) * (ceiling - floor)

        return integral

    # repeat MC integration by mean noRep times and return a list with the results
    def repeatMCMean(self, noRep):

        results = np.linspace(0, 2, noRep)

        for j in range(1, noRep):
            results[j] = self.MCMean()

        return results

        # repeat MC integration by mean noRep times and return a list with the results

    def repeatMCRejection(self, noRep, floor, ceil):

        results = np.linspace(0, 2, noRep)

        for j in range(1, noRep):
            results[j] = self.MCRejection(floor, ceil)

        return results

    def simpsons(self, N):
        sum = 0
        term = 0

        x = np.linspace(self.a, self.b, N)

        # calculating sum
        for i in range(1, N):

            # set weights
            if i == 1 or i == N:
                weight = 1 / 3
            elif i % 2 == 0:
                weight = 4 / 3
            elif i % 2 == 1:
                weight = 2 / 3

            term = self.integrand(x[i]) * weight
            sum = sum + term

        integral = (self.b - self.a) * sum
        return integral


# =====================================

# integral of f(x) = x**2 + x - 1
class integralF1(integralParent):
    def integrand(self, x):
        return x ** 2 + x - 1

    def antiDerivative(self, x):
        return 1 / 3 * x ** 3 + 1 / 2 * x ** 2 - x


# integral of f(x) = cos(x)*log(x)/sqrt(x)
class integralF2(integralParent):
    def integrand(self, x):
        return np.cos(x) * np.log(x) / np.sqrt(x)


# ====================================
N = 10000
noRepeats = 1000

integral1 = integralF1(-10, 10)
print(integral1.analyticalInt())
print(integral1.simpsons(N))


integral2 = integralF2(0, 1)
# print(integral2.MCMean(N))

