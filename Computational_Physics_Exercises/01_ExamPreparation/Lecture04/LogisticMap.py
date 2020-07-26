# %%

import numpy as np
import random
import matplotlib.pyplot as plt


def generatePopulationSequence(initialPopulation, growthParameter, sequenceLength):
    populationSequence = np.empty(sequenceLength)
    populationSequence[:] = np.nan

    populationSequence[0] = initialPopulation

    for generationNumber in range(0, sequenceLength - 1):
        populationSequence[generationNumber + 1] = (
            growthParameter
            * populationSequence[generationNumber]
            * (1 - populationSequence[generationNumber])
        )

    return populationSequence


initialPopulation = 0.75
growthParameters = [0.4, 2.4, 3.2, 3.6, 3.8304]
sequenceLength = 30

for growthParameterIndex in range(0, len(growthParameters)):
    populationSequence = generatePopulationSequence(
        initialPopulation, growthParameters[growthParameterIndex], sequenceLength
    )
    plt.plot(populationSequence)
    plt.show()


# %%


def generateSequencesForBifurcationPlot(Parameters):
    growthParameters = Parameters.growthParameters
    initialPopulations = Parameters.initialPopulations
    initialSequenceLength = Parameters.initialSequenceLength
    keepSequenceLength = Parameters.keepSequenceLength

    growthParameterSequences = np.empty((keepSequenceLength, len(growthParameters)))

    for growthParameterIndex in range(0, len(growthParameters)):
        initialPopulationSequences = np.empty(
            (keepSequenceLength, len(initialPopulations))
        )
        for initialPopulationIndex in range(0, len(initialPopulations)):
            fullSequence = generatePopulationSequence(
                initialPopulations[initialPopulationIndex],
                growthParameters[growthParameterIndex],
                initialSequenceLength + keepSequenceLength,
            )
            initialPopulationSequences[:, initialPopulationIndex] = fullSequence[
                initialSequenceLength:
            ]

        growthParameterSequences[:, growthParameterIndex] = np.average(
            initialPopulationSequences, axis=1
        )

    return growthParameterSequences


class Parameters:
    growthParameters = np.linspace(1, 4, 1001)
    initialPopulations = np.linspace(0, 1, 101)
    initialSequenceLength = 200
    keepSequenceLength = 200


sequences = generateSequencesForBifurcationPlot(Parameters)


# %%

plt.plot(sequences)
plt.show()


# %%


def generatePlotDataFromSequences(Parameters, sequences):
    growthParameters = Parameters.growthParameters
    maximumPointCount = np.size(sequences)
    plotData = np.empty((2, maximumPointCount))
    plotData[:, :] = np.nan

    growthParameterIndex = 0
    plotIndex = 0
    for growthParameterIndex in range(0, len(growthParameters)):
        growthParameter = growthParameters[growthParameterIndex]
        xPoints = removeDuplicates(sequences[:, growthParameterIndex])

        for xPointsIndex in range(0, len(xPoints)):
            plotData[0, plotIndex] = growthParameter
            plotData[1, plotIndex] = xPoints[xPointsIndex]
            plotIndex = plotIndex + 1

    return plotData[:, 0:plotIndex]


def removeDuplicates(sequence):
    roundedSequence = np.around(sequence, 9)
    noDuplicatesSequence = list(set(roundedSequence))
    return noDuplicatesSequence


plotData = generatePlotDataFromSequences(Parameters, sequences)


# %%

plt.scatter(plotData[0, :], plotData[1, :], linewidths=0.1)
plt.show()


# %%
