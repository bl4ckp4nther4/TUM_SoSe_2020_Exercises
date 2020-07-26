# %%

import numpy as np
import random
import matplotlib.pyplot as plt


def getStartingPointInsideTriangle(vertices):

    point = [random.random(), 2 * random.random()]

    while isPointInsideTriangle(point, vertices) == False:
        point = [random.random(), 2 * random.random()]

    return point


def isPointInsideTriangle(point, vertices):
    middlePoint = getMiddlePoint(vertices)
    if arePointsBetweenSameFunctions(point, middlePoint, vertices) == True:
        return True
    else:
        return False


def arePointsBetweenSameFunctions(pointA, pointB, vertices):
    betweenSame = np.empty(3)
    for index in range(0, 3):
        if (pointA[1] <= getBorderFunction(index, vertices, pointA[0])) and (
            pointB[1] <= getBorderFunction(index, vertices, pointB[0])
        ):
            betweenSame[index] = True
        elif (pointA[1] >= getBorderFunction(index, vertices, pointA[0])) and (
            pointB[1] >= getBorderFunction(index, vertices, pointB[0])
        ):
            betweenSame[index] = True
        else:
            betweenSame[index] = False
    if sum(betweenSame) == 3:
        return True
    else:
        return False


def getMiddlePoint(vertices):
    middleX = np.average(vertices[:, 0])
    middleY = np.average(vertices[:, 1])
    middlePoint = [middleX, middleY]
    return middlePoint


def getBorderFunction(index, vertices, x):
    indexPlus = (index + 1) % 3
    slope = (vertices[indexPlus, 0] - vertices[index, 0]) / (
        vertices[indexPlus, 1] - vertices[index, 1]
    )
    axisCross = vertices[index, 0] - slope * vertices[index, 1]

    return slope * x + axisCross


# %%

vertices = np.empty((3, 2))

vertices[0, :] = [1, 1]
vertices[1, :] = [0, 2]
vertices[2, :] = [0, 0]

# %%

middlePoint = getMiddlePoint(vertices)

print(middlePoint)

x = np.linspace(0, 2, 101)

startingPoint = getStartingPointInsideTriangle(vertices)

plt.plot(x, getBorderFunction(0, vertices, x))
plt.plot(x, getBorderFunction(1, vertices, x))
plt.plot(x, getBorderFunction(2, vertices, x))
plt.scatter(vertices[:, 1], vertices[:, 0])
plt.scatter(middlePoint[1], middlePoint[0])
plt.scatter(startingPoint[1], startingPoint[0])
plt.show()


# %%


def getNextPoint(point, vertices):
    randomIndex = random.randint(0, 2)
    nextPointX = np.average([point[0], vertices[randomIndex, 0]])
    nextPointY = np.average([point[1], vertices[randomIndex, 1]])

    return [nextPointX, nextPointY]


def getSierpinskyTrianglePoints(pointCount, vertices):
    allPoints = np.empty((pointCount, 2))
    allPoints[0, :] = getStartingPointInsideTriangle(vertices)
    for pointNumber in range(0, pointCount - 1):
        allPoints[pointNumber + 1, :] = getNextPoint(allPoints[pointNumber], vertices)

    return allPoints


points = getSierpinskyTrianglePoints(10000, vertices)

plt.scatter(points[:, 1], points[:, 0])
plt.show()

# %%
