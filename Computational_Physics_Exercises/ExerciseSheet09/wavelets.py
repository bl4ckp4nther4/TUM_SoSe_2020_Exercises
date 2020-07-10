import numpy as np
import matplotlib.pyplot as plt

# ========================================================================================


def greenBox(C0, C1, C2, C3):
    matrix = np.matrix([[C0, C1, C2, C3], [C3, -C2, C1, -C0]])

    return matrix


def matrixA(rows):
    if rows % 1 != 0:
        print("rows in matrixA has to be an integer")
    rows = int(rows)
    C0 = 0.482963
    C1 = 0.836516
    C2 = 0.224144
    C3 = -0.12941
    GB = greenBox(C0, C1, C2, C3)

    matrixA = np.zeros((rows, rows))
    if rows % 2 == 0:
        steps = int(rows / 2)
    else:
        print("Number of rows must be multiple of two")
    for i in range(0, steps):
        xShift = i * 2
        yShift = i * 2
        if i == steps - 1:
            matrixA[xShift : xShift + 2, yShift : yShift + 2] = GB[0:2, 0:2]
            matrixA[xShift : xShift + 2, 0:2] = GB[0:2, 2:4]
        else:
            matrixA[xShift : xShift + 2, yShift : yShift + 4] = GB

    return matrixA


def reversableConditionMatrix():
    return np.dot(matrixA(4), np.transpose(matrixA(4)))


# =========================================================================================


def exercise1a():
    print("\nShould yield the 1 matrix (reversable Condition):")
    print(reversableConditionMatrix())

    matrix = matrixA(4)
    print(matrix)
    print("\nShould print 0 as second element (detail) for the linear signal:")
    print(np.dot(matrix, np.matrix([[0], [1], [2], [3]])))
    print("\nShould print 0 as second element (detail) for the constant signal:")
    print(np.dot(matrix, np.matrix([[0], [0], [0], [0]])))


# =========================================================================================


def reorder(mixedDetailSmooth):
    L = len(mixedDetailSmooth)

    if L % 2 != 0:
        print("error in reorder, length is not even")

    S = np.empty(int(L / 2))
    D = np.empty(int(L / 2))

    for i in range(0, L):
        if i % 2 == 0:
            S[int(i / 2)] = mixedDetailSmooth[i]
        if i % 2 == 1:
            D[int((i - 1) / 2)] = mixedDetailSmooth[i]

    orderedDetailSmooth = np.concatenate((S, D), axis=None)
    return orderedDetailSmooth


def D4WT(N, y):
    if np.log2(N / 4) % 1 != 0:
        print("\nD4WT: Error, N does not fit")
        return np.log2(N / 4)

    L = N
    smooth = y
    result = np.empty(N)
    while L >= 4:
        matrix = matrixA(L)  # set the transormation matrix
        newSortedVector = reorder(
            np.dot(matrix, smooth)
        )  # calculate and sort new vector

        smooth = newSortedVector[0 : int(L / 2)]  # set the new vector to be transformed
        newDetail = newSortedVector[
            int(L / 2) : int(L)
        ]  # set the new detail vector to be added to result
        result[int(L / 2) : int(L)] = newDetail  # save the detail in results vector

        # plot results
        plt.plot(smooth)
        plt.plot(newDetail)
        plt.show()

        L = L / 2  # set L for the next iteration
    result[0:2] = smooth  # set the last two
    plt.plot(result)
    plt.show()
    return result


# =========================================================================================


def exercise1c():
    sampleSizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    for k in range(0, 9):

        t = np.linspace(0, 1, sampleSizes[k])
        Y = np.sin(60 * t ** 2)
        plt.plot(Y)
        plt.show()

        transfomedSin = D4WT(sampleSizes[k], Y)


# =========================================================================================


def revD4WT(N, Y):
    if np.log2(N / 4) % 1 != 0:
        print("\nD4WT: Error, N does not fit")
        return np.log2(N / 4)

    L = 4

    while L <= N:
        orderedY = Y[
            0 : int(L)
        ]  # transform the part of Y which is half smooth and half detail

        mixedY = revReorder(orderedY)
        matrix = np.transpose(matrixA(L))  # set the transormation matrix

        # set for next iteration
        smooth = np.dot(matrix, mixedY)
        plt.plot(smooth)
        plt.show()

        Y[0 : int(L)] = smooth
        L = L * 2
    y = Y
    return y


def revReorder(orderedDetailSmooth):
    L = len(orderedDetailSmooth)

    if L % 2 != 0:
        print("error in reorder, length is not even")

    S = orderedDetailSmooth[0 : int(L / 2)]
    D = orderedDetailSmooth[int(L / 2) : int(L)]

    mixedDetailSmooth = np.empty(int(L))

    for i in range(0, L):
        if i % 2 == 0:
            mixedDetailSmooth[i] = S[int(i / 2)]
        if i % 2 == 1:
            mixedDetailSmooth[i] = D[int((i - 1) / 2)]

    return mixedDetailSmooth


# =========================================================================================


def exercise1d():
    sampleSize = 1024

    t = np.linspace(0, 1, sampleSize)
    Y = np.sin(60 * t ** 2)
    transformedSin = D4WT(sampleSize, Y)

    revTransformedSin = revD4WT(sampleSize, transformedSin)

    plt.plot(transformedSin)
    plt.plot(revTransformedSin)
    plt.show()


# =========================================================================================


def exercise1e():
    sampleSize = [16, 64, 512]

    for k in range(0, 3):
        Y = np.zeros(sampleSize[k])
        Y[5] = 1
        baseWavelet = revD4WT(sampleSize[k], Y)


# =========================================================================================


exercise1e()
