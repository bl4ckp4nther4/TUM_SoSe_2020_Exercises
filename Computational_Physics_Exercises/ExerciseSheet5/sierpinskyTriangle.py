import numpy as np
import random as rand
import matplotlib.pyplot as plt


class sierpinskiTriangle():

    # number of points inside the triangle
    N = 10

    # vertices; corner points of the triangle
    vertex = np.zeros((2, 3))
    vertex[:, 0] = [0, 1]
    vertex[:, 1] = [1, 0]
    vertex[:, 2] = [-1, 0]

    # starting point
    p = [0.2, 0.2]

    # points inside the triangle
    points = np.zeros((2, 11))

    def __init__(self, N):
        self.N = N
        self.setPoints(self.N)

    def setPoints(self, N):
        # generate points of the sierpinsky triangle
        self.p = [rand.random(), rand.random()]
        self.points = np.zeros((2, self.N+1))
        self.points[:, 0] = self.p

        # generate the points
        for i in range(1, N):
            j = int(np.ceil(rand.random()*3) - 1)
            self.p = 1/2 * (self.p + self.vertex[:, j])
            self.points[:, i] = self.p

    def plotPoints(self):
        plt.scatter(self.points[0, :], self.points[1, :], s=0.1)
        plt.show()


ST = sierpinskiTriangle(100000)
ST.plotPoints()
