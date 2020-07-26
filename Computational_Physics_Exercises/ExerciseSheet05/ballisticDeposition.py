# %%

import numpy as np
import random
from matplotlib import pyplot as plt


def isHole(depositionHeight, depositionLocation):
    locationPlus = (depositionLocation + 1) % len(depositionHeight)
    locationMinus = (depositionLocation - 1) % len(depositionHeight)
    if (
        depositionHeight[depositionLocation] < depositionHeight[locationMinus]
        and depositionHeight[depositionLocation] < depositionHeight[locationPlus]
    ):
        return True


def fillHole(depositionHeight, depositionLocation):
    locationPlus = (depositionLocation + 1) % len(depositionHeight)
    locationMinus = (depositionLocation - 1) % len(depositionHeight)
    depositionHeight[depositionLocation] = max(
        (depositionHeight[locationPlus], depositionHeight[locationMinus],)
    )
    return depositionHeight


def depositParticles(depositionSiteCount, particleCount):
    averageHeight = np.zeros(particleCount)
    depositionHeight = np.zeros(depositionSiteCount)
    depositionSiteMatrix = np.zeros((depositionSiteCount * 2, depositionSiteCount))

    for particleNumber in range(1, particleCount):
        depositionLocation = random.randint(0, depositionSiteCount - 1)

        if isHole(depositionHeight, depositionLocation) == True:
            depositionHeight = fillHole(depositionHeight, depositionLocation)
        else:
            depositionHeight[depositionLocation] = (
                depositionHeight[depositionLocation] + 1
            )

        averageHeight[particleNumber] = sum(depositionHeight) / depositionSiteCount

        depositionSiteMatrix = addNewParticleToMatrix(
            depositionSiteMatrix, depositionHeight
        )
        if particleNumber % 100 == 0:
            fileName = (
                "Computational_Physics_Exercises/ExerciseSheet05/depositionSequence/particle"
                + str(particleNumber)
            )
            writeMatrixToFile(depositionSiteMatrix, fileName)

    croppedDepositionSiteMatrix = cropNonZeros(depositionSiteMatrix)

    return croppedDepositionSiteMatrix


def writeMatrixToFile(matrix, fileName):
    plt.imshow(matrix)
    plt.axis("off")
    plt.savefig(fileName, bbox_inches="tight")


def cropNonZeros(fullMatrix):
    coordinatesWithParticles = np.argwhere(fullMatrix)
    xMin, yMin = coordinatesWithParticles.min(axis=0)
    xMax, yMax = coordinatesWithParticles.max(axis=0)
    croppedMatrix = fullMatrix[xMin : xMax + 1, yMin : yMax + 1]
    return croppedMatrix


def addNewParticleToMatrix(depositionSiteMatrix, depositionHeight):
    for index in range(0, len(depositionHeight)):
        height = int(depositionHeight[index])
        depositionSiteMatrix[height, index] = 1

    return depositionSiteMatrix


# %%
depositionSiteCount = 256

particleCount = depositionSiteCount ** 2

depositionsMatrix = depositParticles(depositionSiteCount, particleCount)

# %%
plt.imshow(depositionsMatrix)
plt.axis("off")
plt.savefig("Result.png", bbox_inches="0")
# %%
