import numpy as np
import matplotlib.pyplot as plt
import random as rand


class diffEqFreePendulum():
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


class timeEvolutionFreePendulum(diffEqFreePendulum):
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

    def timePlot(self):
        plt.plot(self.timeSeq, self.positionSeq)
        plt.xlabel("time in sec")
        plt.ylabel("position")
        plt.show()


class timeEvolutionFrictionPendulum(timeEvolutionFreePendulum):
    alpha = 0.1

    def __init__(self, omega0, alpha, tMax, initPos, initSpeed):
        self.alpha = alpha

        timeEvolutionFreePendulum.__init__(
            self, omega0, tMax, initPos, initSpeed)


class timeEvolutionFrictionAndForce(timeEvolutionFrictionPendulum):
    f = 1
    omega = 2

    def __init__(self, omega0, alpha, f, omega, tMax, initPos, initSpeed):
        self.f = f
        self.omega = omega
        timeEvolutionFrictionPendulum.__init__(
            self, omega0, alpha, tMax, initPos, initSpeed)


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

    def phasePlot(self):
        plt.scatter(self.positionSequences, self.speedSequences, s=0.05)
        plt.show()


class phaseSpaceFrictionPendulum(phaseSpaceFreePendulum):
    alpha = 0.1

    def __init__(self, omega0, alpha, tMax, xMax, yMax, noOfSequences):
        self.alpha = alpha
        phaseSpaceFreePendulum.__init__(self,
                                        omega0, tMax, xMax, yMax, noOfSequences)


class phaseSpaceFrictionAndForce(phaseSpaceFrictionPendulum):
    f = 1
    omega = 2

    def __init__(self, omega0, alpha, f, omega, tMax, xMax, yMax, noOfSequences):
        self.f = f
        self.omega = omega
        phaseSpaceFrictionPendulum.__init__(self,
                                            omega0, alpha, tMax, xMax, yMax, noOfSequences)


# =============================================================================


def exercise2a1():
    freePendulumSmallDisplacement = timeEvolutionFreePendulum(1, 10, 0.1, 0)
    freePendulumSmallDisplacement.timePlot()


def exercise2a2():
    freePendulumLargeDisplacement = timeEvolutionFreePendulum(1, 10, 0.1, 0)
    freePendulumLargeDisplacement.timePlot()


def exercise2a3():
    freePendulumPhaseSpace = phaseSpaceFreePendulum(1, 100, 1, 0, 1)
    freePendulumPhaseSpace.phasePlot()


def exercise2b():
    freePendulumPhaseSpace = phaseSpaceFreePendulum(1, 100, 5, 5, 100)
    freePendulumPhaseSpace.phasePlot()


def exercise2c1():
    withFriction = timeEvolutionFrictionPendulum(1, 0.1, 100, 1, 0)
    withFriction.timePlot()


def exercise2c2():
    withFriction = phaseSpaceFrictionPendulum(1, 0.1, 100, 5, 5, 100)
    withFriction.phasePlot()


def exercise2d1():
    frictionForce = timeEvolutionFrictionAndForce(1, 0.1, 0.2, 0.6, 100, 1, 0)
    frictionForce.timePlot()


def exercise2d2():
    frictionForce = phaseSpaceFrictionAndForce(
        1, 0.1, 0.2, 0.6, 100, 5, 5, 100)
    frictionForce.phasePlot()


def exercise2d3():
    frictionForce = timeEvolutionFrictionAndForce(1, 0.1, 0.8, 0.6, 100, 1, 0)
    frictionForce.timePlot()


def exercise2d4():
    frictionForce = phaseSpaceFrictionAndForce(
        1, 0.1, 0.6, 0.6, 100, 5, 5, 100)
    frictionForce.phasePlot()


# ==============================================================================


exercise2d4()
