import numpy as np
import matplotlib.pyplot as plt

# ========================================================================================


def getGreenBox():
    constant0 = 0.482963
    constant1 = 0.836516
    constant2 = 0.224144
    constant3 = -0.12941
    matrix = np.matrix(
        [
            [constant0, constant1, constant2, constant3],
            [constant3, -constant2, constant1, -constant0],
        ]
    )

    return matrix


def getDiscreteWaveletMatrix(rows):
    if rows % 1 != 0:
        print("rows in matrixA has to be an integer")
    rows = int(rows)
    if rows % 2 == 0:
        greenBoxCount = int(rows / 2)
    else:
        print("Number of rows must be multiple of two")

    greenBox = getGreenBox()

    discreteWaveletMatrix = np.zeros((rows, rows))
    for greenBoxIndex in range(0, greenBoxCount):
        xShift = greenBoxIndex * 2
        yShift = greenBoxIndex * 2
        if greenBoxIndex == greenBoxCount - 1:
            discreteWaveletMatrix[xShift : xShift + 2, yShift : yShift + 2] = greenBox[
                0:2, 0:2
            ]
            discreteWaveletMatrix[xShift : xShift + 2, 0:2] = greenBox[0:2, 2:4]
        else:
            discreteWaveletMatrix[xShift : xShift + 2, yShift : yShift + 4] = greenBox

    return discreteWaveletMatrix


def isFilterReversable():
    matrixTimesTransposed = np.dot(
        getDiscreteWaveletMatrix(4), np.transpose(getDiscreteWaveletMatrix(4))
    )
    identityMatrix = np.identity(4)
    if (np.around(matrixTimesTransposed, 5) == identityMatrix).all():
        print(
            "\nFilter is reversable since the transformation matrix times its own transposed yields the identity matrix"
        )
        return True
    else:
        print(matrixTimesTransposed)
        return False


def doesHighPassFilterWork():
    transformationMatrix = getDiscreteWaveletMatrix(4)
    filteredLinearSignal = np.dot(transformationMatrix, np.matrix([[0], [1], [2], [3]]))
    filteredFlatSignal = np.dot(transformationMatrix, np.matrix([[0], [0], [0], [0]]))
    detailLinearSignal = np.around(filteredLinearSignal[1], 5)
    detailFlatSignal = np.around(filteredFlatSignal[1], 5)
    if detailLinearSignal == 0 and detailFlatSignal == 0:
        print("\nHigh pass filter (detail) gives 0 for the flat and linear signals")
        return True
    else:
        print("\n", detailFlatSignal, detailLinearSignal)
        return False


# =========================================================================================


def getFilteredSignal(filterMatrix, smoothSignal):
    filteredSignal = np.dot(filterMatrix, smoothSignal)
    return filteredSignal


def alternatingToSeparated(alternatingDetailSmooth):
    length = len(alternatingDetailSmooth)

    if length % 2 != 0:
        print("error in reorder, length is not even")

    smooth = np.empty(int(length / 2))
    detail = np.empty(int(length / 2))

    for index in range(0, length):
        if index % 2 == 0:
            smooth[int(index / 2)] = alternatingDetailSmooth[index]
        if index % 2 == 1:
            detail[int((index - 1) / 2)] = alternatingDetailSmooth[index]

    separatedDetailSmooth = np.concatenate((smooth, detail), axis=None)
    return separatedDetailSmooth


def getSmoothPartFromFiltered(alternatingDetailSmooth):
    separatedDetailSmooth = alternatingToSeparated(alternatingDetailSmooth)
    smoothPart = separatedDetailSmooth[: int(len(separatedDetailSmooth) / 2)]
    return smoothPart


def getDetailPartFromFiltered(alternatingDetailSmooth):
    separatedDetailSmooth = alternatingToSeparated(alternatingDetailSmooth)
    detailPart = separatedDetailSmooth[int(len(separatedDetailSmooth) / 2) :]
    return detailPart


def getDiscreteWaveletTransform(initialSignal, plot=False):
    signalLength = len(initialSignal)
    if np.log2(signalLength / 4) % 1 != 0:
        print(
            "\ngetDiscreteWaveletTransform: Error, initialFunction has to be of length 4*n"
        )
        return np.log2(signalLength / 4)

    transformedSignal = np.empty(signalLength)
    smoothPart = np.copy(initialSignal)
    filterMatrixSize = signalLength
    while filterMatrixSize >= 4:
        filterMatrix = getDiscreteWaveletMatrix(filterMatrixSize)
        filteredSignal = getFilteredSignal(filterMatrix, smoothPart)
        smoothPart = getSmoothPartFromFiltered(filteredSignal)
        detailPart = getDetailPartFromFiltered(filteredSignal)
        transformedSignal[
            int(filterMatrixSize / 2) : int(filterMatrixSize)
        ] = detailPart

        filterMatrixSize = filterMatrixSize / 2

        if plot == True:
            plt.plot(smoothPart)
            plt.plot(detailPart)
            plt.show()

    transformedSignal[0:2] = smoothPart  # set the last calculated smooth part
    return transformedSignal


# =========================================================================================


def getInverseDiscreteWaveletTransform(transformedSignal):
    signalLength = len(transformedSignal)
    if np.log2(signalLength / 4) % 1 != 0:
        print(
            "\ngetInverseDiscreteWaveletTransform: Error, initialFunction has to be of length 4*n"
        )
        return np.log2(signalLength / 4)

    filterMatrixSize = 4
    backTransformedSignal = np.copy(transformedSignal)
    while filterMatrixSize <= signalLength:
        smoothPart = backTransformedSignal[0 : int(filterMatrixSize / 2)]
        detailPart = backTransformedSignal[
            int(filterMatrixSize / 2) : int(filterMatrixSize)
        ]
        alternatingSmoothDetail = getAlternatingSmoothDetail(smoothPart, detailPart)

        inverseTransfomationMatrix = np.transpose(
            getDiscreteWaveletMatrix(filterMatrixSize)
        )

        smoothPart = np.dot(inverseTransfomationMatrix, alternatingSmoothDetail)
        backTransformedSignal[0 : int(filterMatrixSize)] = smoothPart

        filterMatrixSize = filterMatrixSize * 2

    return backTransformedSignal


def getInverseFilteredSignal(filterMatrix, smoothPart, detailPart):
    inverseFilteredSignal = np.dot(filterMatrix, [smoothPart, detailPart])
    return inverseFilteredSignal


def getAlternatingSmoothDetail(smoothPart, detailPart):
    length = len(smoothPart) + len(detailPart)

    if length % 2 != 0:
        print("error in reorder, length is not even")

    alternatingSmoothDetail = np.empty(int(length))

    for i in range(0, length):
        if i % 2 == 0:
            alternatingSmoothDetail[i] = smoothPart[int(i / 2)]
        if i % 2 == 1:
            alternatingSmoothDetail[i] = detailPart[int((i - 1) / 2)]

    return alternatingSmoothDetail


# =========================================================================================
def plotSmoothAndDetail(sampleSizes):
    for sampleSize in sampleSizes:
        timePoints = np.linspace(0, 1, sampleSize)
        discreteSignal = signal(timePoints)

        getDiscreteWaveletTransform(discreteSignal, plot=True)


# =========================================================================================


def plotDaub4e5BaseWavelet(sampleSize):
    sample = np.zeros(sampleSize)
    sample[5] = 1
    baseWavelet = getInverseDiscreteWaveletTransform(sample)
    plt.plot(baseWavelet)
    plt.show()


# =========================================================================================


# %%

doesHighPassFilterWork()
isFilterReversable()

# %%


def signal(t):
    return np.sin(60 * t ** 2)


sampleSizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
plotSmoothAndDetail(sampleSizes)

# %%

sampleSize = 128
timeSteps = np.linspace(0, 1, sampleSize)
discreteSignal = signal(timeSteps)
transformedSignal = getDiscreteWaveletTransform(discreteSignal)
inverseSignal = getInverseDiscreteWaveletTransform(transformedSignal)
plt.plot(discreteSignal)
plt.plot(inverseSignal)
plt.show()


# %%

plotDaub4e5BaseWavelet(16)
plotDaub4e5BaseWavelet(64)
plotDaub4e5BaseWavelet(512)
