import numpy as np
import matplotlib.pyplot as plt
import random as rand


class freePendulumDiffEq():
    alpha = 0   # friction
    f = 0       # driving force
    omega = 0   # frequency of the driving force

    omega0 = 1  # angular frequency of the pendulum for small angles
    h = 0.1     # length of one time step

    Y_0 = np.zeros(2)  # vector Y
    Y_0[0] = 0.1  # initial position
    Y_0[1] = 0   # initial speed

    def __init__(self, omega0):
        self.omega0 = omega0

    def diffEq(self, t, Y):
        # system of linked differential equations
        F = np.zeros(2)
        F[0] = Y[1]
        F[1] = -self.omega0**2 * \
            np.sin(Y[0]) - self.alpha*Y[1] + self.f * np.cos(self.omega * t)
        return F


class timeEvolutionFreePendulum(freePendulumDiffEq):
    tMax = 10
    timeSeq = np.zeros(100)
    positionSeq = np.zeros(100)
    speedSeq = np.zeros(100)

    def __init__(self, omega0, tMax, initPos, initSpeed):
        self.omega0 = omega0
        self.tMax = tMax
        self.Y_0[0] = initPos
        self.Y_0[1] = initSpeed

        self.setTimeEvolution(self.Y_0[0], self.Y_0[1])

    def RK4(self, t, Y):
        # Runge Kutta Methode
        k1 = self.h * self.diffEq(t, Y)
        k2 = self.h * self.diffEq(t + self.h/2, Y + k1/2)
        k3 = self.h * self.diffEq(t + self.h/2, Y + k2/2)
        k4 = self.h * self.diffEq(t + self.h, Y + k3)
        return Y + k1/6 + k2/3 + k3/3 + k4/6

    def setTimeEvolution(self, initPos, initSpeed):
        # calculate position and speed for all timesteps
        self.Y_0[0] = initPos
        self.Y_0[1] = initSpeed

        self.timeSeq = np.zeros(int(self.tMax/self.h))
        self.positionSeq = np.zeros(int(self.tMax/self.h))
        self.speedSeq = np.zeros(int(self.tMax/self.h))

        Y = self.Y_0
        for i in range(int(self.tMax/self.h)):
            t = i*self.h
            Y = self.RK4(t, Y)

            self.timeSeq[i] = t
            self.positionSeq[i] = Y[0]
            self.speedSeq[i] = Y[1]

    def plot(self):
        plt.plot(self.timeSeq, self.positionSeq)
        plt.xlabel("time in sec")
        plt.ylabel("position")
        plt.show()


class phaseSpaceFreePendulum(timeEvolutionFreePendulum):
    noOfSequences = 100
    h = 0.01
    tMax = 100
    xMax = 5
    yMax = 5
    timeSequences = np.zeros((100, 100))
    positionSequences = np.zeros((100, 100))
    speedSequences = np.zeros((100, 100))

    def __init__(self, omega0, tMax, xMax, yMax, noOfSequences):
        self.omega0 = omega0
        self.tMax = tMax
        self.xMax = xMax
        self.yMax = yMax

        self.noOfSequences = noOfSequences

        self.setPhaseSpace(self.noOfSequences)

    def setPhaseSpace(self, noOfSequences):
        # calculate positions and speed for all time steps for N

        self.timeSequences = np.zeros(
            (int(self.tMax/self.h), self.noOfSequences))
        self.positionSequences = np.zeros(
            (int(self.tMax/self.h), self.noOfSequences))
        self.speedSequences = np.zeros(
            (int(self.tMax/self.h), self.noOfSequences))

        for i in range(0, self.noOfSequences):
            self.Y_0[0] = rand.random() * 2*self.xMax - self.xMax
            self.Y_0[1] = rand.random() * 2*self.yMax - self.yMax

            self.setTimeEvolution(self.Y_0[0], self.Y_0[1])

            self.timeSequences[:, i] = self.timeSeq
            self.positionSequences[:, i] = self.positionSeq
            self.speedSequences[:, i] = self.speedSeq

    def plot(self):
        plt.scatter(self.positionSequences, self.speedSequences, s=0.5)
        plt.show()


class phaseSpaceFrictionPendulum(phaseSpaceFreePendulum):
    alpha = 0.1

    def __init__(self, omega0, alpha, tMax, xMax, yMax, noOfSequences):
        self.alpha = alpha
        phaseSpaceFreePendulum.__init__(self,
                                        omega0, tMax, xMax, yMax, noOfSequences)


# =============================================================================

def exercies1a1():
    freePendulumSmallDisplacement = timeEvolutionFreePendulum(1, 10, 0.1, 0)
    freePendulumSmallDisplacement.plot()


def exercise1a2():
    freePendulumLargeDisplacement = timeEvolutionFreePendulum(1, 10, 0.1, 0)
    freePendulumLargeDisplacement.plot()


def exercise1a3():
    freePendulumPhaseSpace = phaseSpaceFreePendulum(1, 10, 1, 0, 1)
    freePendulumPhaseSpace.plot()


def exercise1b():
    freePendulumPhaseSpace = phaseSpaceFreePendulum(1, 10, 5, 5, 100)
    freePendulumPhaseSpace.plot()


def exercise1c():
    withFriction = phaseSpaceFrictionPendulum(1, 0.1, 10, 5, 5, 100)
    withFriction.plot()


# ==============================================================================


exercise1c()