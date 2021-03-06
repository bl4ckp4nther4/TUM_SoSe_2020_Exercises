# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# This Script will calculate Quantum Wave Functions via Path Integratin
# with the Metropolis Algorithm

# %%
import numpy as np
import random
import matplotlib.pyplot as plt


# %%
def getLatticeAction(parameters, positions):
    mass = parameters.mass
    a = parameters.a
    timeIntervalsCount = parameters.timeIntervalsCount

    latticeAction = 0
    for timeIndex in range(0, timeIntervalsCount):
        # TODO: add relatice position in potential somehow
        term = mass / (2 * a) * (
            positions[timeIndex + 1] - positions[timeIndex]
        ) ** 2 + a * potential(parameters, positions[timeIndex])
        latticeAction = latticeAction + term

    return latticeAction


# %%
def potential(parameters, position):
    k = parameters.k

    return k * position ** 2 / 2


# %%
def updateConfiguration(parameters, oldPositions):
    timeIntervalsCount = parameters.timeIntervalsCount
    epsilon = parameters.epsilon

    newPositions = np.copy(oldPositions)
    for changePositionIndex in range(0, timeIntervalsCount):
        positionBeforeChange = newPositions[changePositionIndex]
        randomPositionChange = random.uniform(-epsilon, epsilon)

        newPositions[changePositionIndex] = (
            newPositions[changePositionIndex] + randomPositionChange
        )

        if keepConfiguration(parameters, oldPositions, newPositions) == False:
            newPositions[changePositionIndex] = positionBeforeChange

    return newPositions


def keepConfiguration(parameters, oldPositions, newPositions):
    # Metropolis Algorithm: keep configuration with probability depending on the energies / actions
    oldAction = getLatticeAction(parameters, oldPositions)
    newAction = getLatticeAction(parameters, newPositions)
    deltaAction = newAction - oldAction
    probability = np.exp(-deltaAction)
    randomNumber = random.random()

    if randomNumber <= probability:
        return True
    if randomNumber > probability:
        return False


# %%
class parameters:
    k = 1
    mass = 1
    a = 0.5
    epsilon = 1.4
    timeIntervalsCount = 25
    configurationsCount = 300
    correlatedCount = 50
    coldStart = True


# %%
def initializePositions(parameters):
    timeIntervalsCount = parameters.timeIntervalsCount
    coldStart = parameters.coldStart
    epsilon = parameters.epsilon

    if coldStart == False:
        # number of positions has to be one larger than the number of timesteps
        positions = np.empty(timeIntervalsCount + 1)
        for timeIndex in range(0, timeIntervalsCount + 1):
            positions[timeIndex] = epsilon * (2 * random.random() - 1)

        # the last position needs to be equal to the first position
        positions[timeIntervalsCount] = positions[0]

    if coldStart == True:
        # number of positions has to be one larger than the number of timesteps
        positions = np.zeros(timeIntervalsCount + 1)

    return positions


initialConfiguration = initializePositions(parameters)
plt.plot(initialConfiguration)
plt.show()


# %%
def thermalizeConfiguration(parameters, positions):
    updateCount = 10 * parameters.correlatedCount
    for _ in range(0, updateCount):
        positions = updateConfiguration(parameters, positions)

    return positions


thermalizedConfiguration = thermalizeConfiguration(parameters, initialConfiguration)
plt.plot(thermalizedConfiguration)
plt.show()


# %%
def calculateUncorrelatedConfigurations(parameters, configuration):
    timeIntervalsCount = parameters.timeIntervalsCount
    configurationsCount = parameters.configurationsCount
    correlatedCount = parameters.correlatedCount

    uncorrelatedConfigurations = np.empty((timeIntervalsCount + 1, configurationsCount))

    for configurationIndex in range(0, configurationsCount):
        for updateIndex in range(0, correlatedCount):
            configuration = updateConfiguration(parameters, configuration)

        uncorrelatedConfigurations[:, configurationIndex] = configuration

    return uncorrelatedConfigurations


configurationSamples = calculateUncorrelatedConfigurations(
    parameters, thermalizedConfiguration
)
plt.plot(configurationSamples)
plt.show()


# %%
def calculateGreensFunction(parameters, configurationSamples):
    timeIntervalsCount = parameters.timeIntervalsCount
    configurationsCount = parameters.configurationsCount

    greensFunction = np.empty(timeIntervalsCount + 1)

    for timeIndex in range(0, timeIntervalsCount + 1):
        greensFunction[timeIndex] = calculateGreensFunctionTerm(
            configurationSamples, timeIndex
        )

    return greensFunction


def calculateGreensFunctionTerm(configurationSamples, timeIndex):
    timeIntervalsCount = len(configurationSamples[:, 0]) - 1

    greensFunctionTerm = 0
    for timeIndexSum in range(0, timeIntervalsCount + 1):
        term = (
            1
            / (timeIntervalsCount + 1)
            * np.dot(
                configurationSamples[
                    (timeIndex + timeIndexSum) % timeIntervalsCount, :
                ],
                configurationSamples[timeIndexSum, :],
            )
        )

        greensFunctionTerm = greensFunctionTerm + term

    return greensFunctionTerm


greensFunction = calculateGreensFunction(parameters, configurationSamples)
plt.scatter(
    np.linspace(0, parameters.timeIntervalsCount, parameters.timeIntervalsCount + 1),
    greensFunction,
)
plt.show()


# %%
def calculateDeltaEnergy(parameters, greensFunction):
    timeIntervalsCount = parameters.timeIntervalsCount
    a = parameters.a

    deltaEnergy = np.empty(timeIntervalsCount)

    for timeIndex in range(0, timeIntervalsCount):
        deltaEnergy[timeIndex] = (
            1
            / a
            * np.log(np.abs(greensFunction[timeIndex] / greensFunction[timeIndex + 1]))
        )

    return deltaEnergy


deltaEnergy = calculateDeltaEnergy(parameters, greensFunction)


# %%
plotCount = 10

plt.plot(deltaEnergy)
plt.show()


# %%
plt.hist(configurationSamples[0, :])
plt.show()


# %%

