import numpy as np


class newtonRaphson:
    # newton raphson method for finding roots

    SPEEDOFLIGHT = 299792458  # m s*-1
    PLANCKCONSTANT = 6.62607004E-34  # m**2 kg s**-1
    BOLTZMANNCONSTANT = 1.38064852E-23  # m**2 kg s**-2 K**-1

    temperature = 5777  # kelvin
    initialGuess = 1
    N = 100
    rootApproximation = 0

    def __init__(self, x_0, N, temperature):
        self.initialGuess = x_0
        self.N = N
        self.temperature = temperature

        self.setRootApproximation()

    def function(self, x):
        return x

    def functionDerivative(self, x):
        return 1

    def nextTerm(self, x_n):
        return x_n - self.function(x_n)/self.functionDerivative(x_n)

    def setRootApproximation(self):
        x = self.initialGuess
        for i in range(1, self.N+1):
            x = self.nextTerm(x)
        self.rootApproximation = x
        print("x was approximated to: ", self.rootApproximation)


class maxWavelength(newtonRaphson):

    wavelength = 1

    def __init__(self, x_0, N, temperature):
        self.initialGuess = x_0
        self.N = N
        self.temperature = temperature

        self.setRootApproximation()
        self.setWavelength()

    def function(self, x):
        return 5*(1 - np.exp(-x)) - x

    def functionDerivative(self, x):
        return 5*np.exp(-x) - 1

    def setWavelength(self):
        self.wavelength = self.PLANCKCONSTANT*self.SPEEDOFLIGHT / \
            (self.rootApproximation * self.BOLTZMANNCONSTANT * self.temperature)
        print("The wavelength of maximum emission is: ",
              self.wavelength * 10**9,
              " nm")


class maxFrequency(newtonRaphson):

    frequency = 1

    def __init__(self, x_0, N, temperature):
        self.initialGuess = x_0
        self.N = N
        self.temperature = temperature

        self.setRootApproximation()
        self.setFrequency()

    def function(self, y):
        return 3*(1 - np.exp(-y)) - y

    def functionDerivative(self, y):
        return 3*np.exp(-y) - 1

    def setFrequency(self):
        self.frequency = self.BOLTZMANNCONSTANT * self.temperature / \
            self.PLANCKCONSTANT * self.rootApproximation
        print("The frequency of maximum emission is: ",
              self.frequency,
              " Hz")


maxWavelengthSun = maxWavelength(5, 100, 5777)

maxFrequencySun = maxFrequency(3, 100, 5777)

print("Ratio maximum frequency / maximum frequency derived from maximum wavelength by c/lambda: ", maxWavelengthSun.wavelength /
      maxWavelengthSun.SPEEDOFLIGHT * maxFrequencySun.frequency)
