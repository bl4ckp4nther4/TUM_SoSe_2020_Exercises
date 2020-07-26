# %%


import numpy as np
import random
import matplotlib.pyplot as plt

# %%


# calculate the integral of exp(-x) from 0 to infinity


def minusExponentialFunction(x):
    return np.exp(-x)


def exponentialWeightingFunction(lambd, x):
    return np.exp(-x / lambd)


def xScaledToExponential(lambd):
    r = random.random()
    return -lambd * np.log(1 - r)


def calculateMinusExponentialIntegral(lambd, N):
    sum = 0
    for _ in range(0, N):
        x = xScaledToExponential(lambd)
        term = minusExponentialFunction(x) / exponentialWeightingFunction(lambd, x)
        sum = sum + term
    integral = lambd / N * sum

    return integral


lambd = 2
N = 1000000

x = np.linspace(0, 10, 101)

plt.plot(x, minusExponentialFunction(x))
plt.show()

print(calculateMinusExponentialIntegral(lambd, N))

# %%

# calculate the integral of ln(cos(x))/x from 0 to 1


def function(x):
    return np.log(np.cos(x)) / x


def calculateIntegral(N):
    sum = 0
    for _ in range(0, N):
        x = random.random()
        term = function(x)
        sum = sum + term
    integral = sum / N

    return integral


N = 10000

x = np.linspace(0, 1, 101)

plt.plot(x, function(x))
plt.show()

print(calculateIntegral(N))


# %%
