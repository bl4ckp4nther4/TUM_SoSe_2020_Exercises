#!/usr/bin/python

# This program uses the functions update(), S() and MCaverage() from
# Lepage's "Lattice QCD for novices" (hep-lat/0506036) to repeat the
# determination of the HO WF that we already did in Landau ch. 28.
# SR Jun09

# expanded version: We also use Lepage's algorithm for the Green's
# function to determine the excitation energy

# Now also working with Python3 - SR Jul20

import numpy
import pylab
from random import uniform
from math import *
import matplotlib.pyplot as plt


def update(x):
    for j in range(0, N):
        old_x = x[j]  # save original value
        old_Sj = S(j, x)
        x[j] = x[j] + uniform(-eps, eps)  # update x[j]
        dS = S(j, x) - old_Sj  # change in action
        if dS > 0 and exp(-dS) < uniform(0, 1):
            x[j] = old_x  # restore old value
        place = int(M / xscale * x[j] + M / 2)
        if 0 <= place < M:
            prop[place] += 1


def S(j, x):  # harm. osc. S
    jp = (j + 1) % N  # next site
    jm = (j - 1) % N  # previous site
    return a * x[j] ** 2 / 2 + x[j] * (x[j] - x[jp] - x[jm]) / a


def compute_G(x, n):
    g = 0
    for j in range(0, N):
        g = g + x[j] * x[(j + n) % N]
    return g / N


def MCaverage(x, G):
    for j in range(0, N):  # initialize x
        x[j] = 0
    for j in range(0, 5 * N_cor):  # thermalize x
        update(x)
    for alpha in range(0, N_cf):  # loop on random paths
        for j in range(0, N_cor):
            update(x)
        for n in range(0, N):
            G[alpha][n] = compute_G(x, n)
        plt.plot(x)
    plt.show()
    avg_G = numpy.empty(N)
    for n in range(0, N):  # compute MC averages
        avg_G[n] = 0
        for alpha in range(0, N_cf):
            avg_G[n] = avg_G[n] + G[alpha][n]
        print("G(%d) = %g" % (n, avg_G[n] / N_cf))

    plt.plot(avg_G)
    plt.show()


def avg(G):
    return sum(G) / len(G)


def deltaE(G):
    avgG = avg(G)
    adE = numpy.log(numpy.abs(avgG[:-1] / avgG[1:]))
    return adE / a


# set parameters:
N = 25
N_cor = 50
N_cf = 300
a = 0.5
eps = 1.4
M = 100
xscale = 10

# create arrays:
x = numpy.zeros((N,), numpy.float)
G = numpy.zeros((N_cf, N), numpy.float)
prop = numpy.zeros((M,), numpy.float)

# do the simulation:
MCaverage(x, G)

pylab.plot(prop)
pylab.show()

print("DeltaE is ", deltaE(G))

pylab.scatter(range(N - 1), deltaE(G))
pylab.show()
