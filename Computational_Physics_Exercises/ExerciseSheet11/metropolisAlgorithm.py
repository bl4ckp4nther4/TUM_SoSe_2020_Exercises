import numpy as np
import random
import matplotlib.pyplot as plt
import sys


class progressBar:
    toolbarWidth = 100
    lastUpdate = 0

    def __init__(self):
        self.toolbarWidth = 100

        # setup toolbar
        sys.stdout.write("[%s]" % (" " * self.toolbarWidth))
        sys.stdout.flush()
        sys.stdout.write(
            "\b" * (self.toolbarWidth + 1)
        )  # return to start of line, after '['

    def updateBar(self, progress):
        progressBits = progress * self.toolbarWidth

        delta = int(np.floor(progressBits) - self.lastUpdate)
        for i in range(0, delta):
            sys.stdout.write("-")
            sys.stdout.flush()
        self.lastUpdate = np.floor(progressBits)

    def finishBar(self):
        sys.stdout.write("]\n")


def potential(x):
    return x ** 2 / 2


def changePos(posValue, epsilon):  # flip a dipole value
    return posValue + random.random() * epsilon * 2 - epsilon


def configPlot(config):  # output the current config
    print(config)


def configAction(config,):  # config energy of the ising chain in Joule
    N = len(config) - 1

    sum = 0
    term = 0

    for i in range(0, N):  # go through the sum
        term = (config[i + 1] - config[i]) ** 2 + 0.5 * potential(config[i])

        sum = sum + term
    # calculate energy from the sum with J = 1
    action = sum  # config energy in Joule
    return action


def configProbability(oldConfig, newConfig):
    # probability of trial config to be accepted
    dAction = deltaAction(oldConfig, newConfig)
    probability = np.exp(-(dAction))
    return probability


def deltaAction(oldConfig, newConfig):
    oldAction = configAction(oldConfig)
    newAction = configAction(newConfig)
    deltaAction = newAction - oldAction
    return deltaAction


def setConfig(N, coldStart):
    config = np.empty(N + 1)

    config[0] = 0
    config[N] = 0

    # initial setup ising chain
    for i in range(1, N):  # set dipoles randomly to 1 or -1
        if coldStart:
            position = 0
        else:
            position = random.random() * 2 - 1

        config[i] = position
    return config


def updateConfig(oldConfig, epsilon):
    # set trial config to current config

    N = len(oldConfig) - 1

    changePosNo = random.randint(0, N)

    # change the position
    trialConfig = oldConfig
    trialConfig[changePosNo] = changePos(trialConfig[changePosNo], epsilon)

    if deltaAction(oldConfig, trialConfig) < 0:
        newConfig = trialConfig
    else:
        # calculate probabiliy from the configs via Action
        p = configProbability(oldConfig, trialConfig)

        # generate random number r between 0 and 1
        r = random.random()
        # decide if trial config is accepted
        if p >= r:
            # accept trial config
            newConfig = trialConfig
        else:
            # dont change Config
            newConfig = oldConfig
    return newConfig


def termalizeConfig(config, iterations, epsilon):
    N = len(config) - 1
    allConfigs = np.empty((N + 1, iterations + 1))
    allConfigs[:, 0] = config

    for i in range(1, iterations + 1):
        allConfigs[:, i] = updateConfig(allConfigs[:, i - 1], epsilon)
    return allConfigs


def metropolisAlgorith(
    N, steps, coldStart, epsilon
):  # this algorithm calculates a valid ising chain of N elemets

    # declarations
    oldConfig = np.empty(N + 1)  # Ising chain: with current config
    newConfig = np.empty(N + 1)  # Ising chain: with trial config

    oldConfig[0] = 0
    oldConfig[N] = 0

    # initial setup ising chain
    for i in range(1, N):  # set dipoles randomly to 1 or -1
        if coldStart:
            position = 0
        else:
            position = random.random() * 20 - 10

        oldConfig[i] = position

    # generate trial configs and decide to accept or deny

    for i in range(0, steps):

        # set trial config to current config
        newConfig = oldConfig

        # 1b) pick one random dipole
        changePosNo = random.randint(0, N)

        # flip the dipole
        newConfig[changePosNo] = changePos(newConfig[changePosNo], epsilon)

        if deltaAction(oldConfig, newConfig) < 0:
            oldConfig = newConfig
        else:
            # calculate probabiliy from the configs via Action
            p = configProbability(oldConfig, newConfig)

            # generate random number r between 0 and 1
            r = random.random()
            # decide if trial config is accepted
            if p >= r:
                # accept trial config
                oldConfig = newConfig

    return oldConfig


N = 100

Ncf = 5000
Ncr = 50

epsilon = 1.4

config = setConfig(N, coldStart=False)

allConfigs = termalizeConfig(config, Ncf * Ncr, epsilon)

bar = progressBar()

uncorrConfigs = np.empty((N + 1, Ncf))
for l in range(0, Ncf):
    # take every 50th configuration
    uncorrConfigs[:, l] = allConfigs[:, (l + 1) * Ncr]
    bar.updateBar((l + 1) / Ncf)

bar.finishBar()
plt.plot(uncorrConfigs)
plt.show()
