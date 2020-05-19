import numpy as np
import matplotlib.pyplot as plt


E0 = 2.17896E-18
kB = 1.38064852E-23
T = 300


def E(n):
    return -E0/n**2


def bolzmannDistribution(n, T):
    term = 1
    sum = 0

    m = 0
    while sum / term < 10**20:
        m = m + 1
        term = m**2 * np.exp(E(n) - E(m) / (kB*T))
        sum = sum + term

    p = n**2 / sum
    return p


print(bolzmannDistribution(1, 300))
