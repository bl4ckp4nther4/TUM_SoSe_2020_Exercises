import numpy as np
import random
import matplotlib.pyplot as plt


def generateInitialConfiguration(Parameters):
    chainLength = Parameters.chainLength
    warmStart = Parameters.warmStart

    initialConfiguration = np.zeros(chainLength)

    if warmStart == True:
        for index in range(0, chainLength):
            initialConfiguration[index] = 2 * random.randint(0, 1) - 1
    elif warmStart == False:
        initialConfiguration = initialConfiguration + 2 * random.randint(0, 1) - 1
    return initialConfiguration


def updateConfiguration(oldConfiguration, Parameters):
    trialConfiguration = changeRandomSpin(oldConfiguration)

    keepConfiguration = keepTrialConfiguration(
        oldConfiguration, trialConfiguration, Parameters
    )
    if keepConfiguration == True:
        return trialConfiguration
    elif keepConfiguration == False:
        return oldConfiguration
    else:
        print("updateConfiguration returns None")
        print("updateConfiguration returns None")


def changeRandomSpin(oldConfiguration):
    chainLength = len(oldConfiguration)
    trialConfiguration = np.copy(oldConfiguration)
    randomSpinPosition = random.randint(0, chainLength - 1)
    newSpin = flipSpin(oldConfiguration[randomSpinPosition])
    trialConfiguration[randomSpinPosition] = newSpin
    return trialConfiguration


def flipSpin(spinValue):
    if spinValue == 1:
        return -1
    if spinValue == -1:
        return 1


def keepTrialConfiguration(oldConfiguration, trialConfiguration, Parameters):
    exchangeEnergy = Parameters.exchangeEnergy
    temperatureEnergy = Parameters.temperatureEnergy

    oldEnergy = calculateEnergy(oldConfiguration, exchangeEnergy)
    trialEnergy = calculateEnergy(trialConfiguration, exchangeEnergy)
    deltaEnergy = trialEnergy - oldEnergy

    probabilityToKeep = np.exp(-deltaEnergy / temperatureEnergy)
    randomNumber = random.random()

    if probabilityToKeep >= randomNumber:
        return True
    elif probabilityToKeep < randomNumber:
        return False
    else:
        print("keepTrialConfiguration returns None")


def calculateEnergy(configuration, exchangeEnergy):
    chainLength = len(configuration)
    sum = 0
    for index in range(0, chainLength):
        indexPlus = (index + 1) % chainLength
        term = configuration[index] * configuration[indexPlus]
        sum = sum + term

    configurationEnergy = -exchangeEnergy * sum

    return configurationEnergy


def calculateMagnetization(configuration):
    chainLength = len(configuration)
    magnetization = 0
    for index in range(0, chainLength):
        term = configuration[index]
        magnetization = magnetization + term

    return magnetization


def calculateInternalEnergy(configuration, Parameters):
    chainLength = len(configuration)
    internalEnergy = (
        calculateEnergy(configuration, Parameters.exchangeEnergy) / chainLength
    )

    return internalEnergy


def printConfiguration(configuration):
    chainLength = len(configuration)
    configurationString = ""

    for index in range(0, chainLength):
        if configuration[index] == 1:
            configurationString = configurationString + "+"
        if configuration[index] == -1:
            configurationString = configurationString + "-"

    print(configurationString)


def thermalizeConfiguration(configuration, Parameters):
    magnetization = np.zeros(Parameters.thermalizeUpdateCount)
    internalEnergy = np.zeros(Parameters.thermalizeUpdateCount)

    for thermalizationProgress in range(0, Parameters.thermalizeUpdateCount):
        configuration = updateConfiguration(configuration, Parameters)
        magnetization[thermalizationProgress] = calculateMagnetization(configuration)
        internalEnergy[thermalizationProgress] = calculateInternalEnergy(
            configuration, Parameters
        )

    thermalizationResults = dict()
    thermalizationResults["magnetization"] = magnetization
    thermalizationResults["internalEnergy"] = internalEnergy
    thermalizationResults["configuration"] = configuration

    return thermalizationResults


def generateAverageResults(Parameters):
    averageOverCount = Parameters.averageOverCount
    chainLength = Parameters.chainLength
    thermalizeUpdateCount = Parameters.thermalizeUpdateCount

    totalMagnetization = np.zeros(thermalizeUpdateCount)
    totalInternalEnergy = np.zeros(thermalizeUpdateCount)
    configurations = np.zeros((chainLength, averageOverCount))

    for averageProgress in range(0, averageOverCount):
        results = generateOneConfiguration(Parameters)
        configurations[:, averageProgress] = results["configuration"]
        totalMagnetization = totalMagnetization + results["magnetization"]
        totalInternalEnergy = totalInternalEnergy + results["internalEnergy"]

    averageMagnetization = totalMagnetization / averageOverCount
    averageInternalEnergy = totalInternalEnergy / averageOverCount

    averageResults = dict()
    averageResults["averageMagnetization"] = averageMagnetization
    averageResults["averageInternalEnergy"] = averageInternalEnergy

    return averageResults


def generateOneConfiguration(Parameters):
    initialConfiguration = generateInitialConfiguration(Parameters)
    results = thermalizeConfiguration(initialConfiguration, Parameters)

    return results


class Parameters:
    chainLength = 100
    warmStart = False
    thermalizeUpdateCount = 10 * chainLength
    exchangeEnergy = -1
    temperatureEnergy = 1
    averageOverCount = 100


initialConfiguration = generateInitialConfiguration(Parameters)
thermalizedResult = thermalizeConfiguration(initialConfiguration, Parameters)
printConfiguration(thermalizedResult["configuration"])

# average Results

averageResults = generateAverageResults(Parameters)

# conpare average to one result

plt.plot(thermalizedResult["magnetization"])
plt.plot(averageResults["averageMagnetization"])
plt.show()
plt.plot(thermalizedResult["internalEnergy"])
plt.plot(averageResults["averageInternalEnergy"])
plt.show()
