import numpy as np
import matplotlib.pyplot as plt
import random as rand


class diffEqPendulum():
    __omega0 = 1  # angular frequency of the pendulum for small angles
    __alpha = 0   # friction
    __f = 0       # driving force
    __omega = 0   # frequency of the driving force

    __tMax = 10       # total time length
    __tStep = 0.1     # length of one time step

    __Y_0 = np.zeros(2)  # vector Y
    __Y_0[0] = 0.1  # initial position
    __Y_0[1] = 0   # initial speed

    timeSeq = np.zeros(100)
    positionSeq = np.zeros(100)
    speedSeq = np.zeros(100)

    def __init__(self, omega0, alpha, f, omega):
        self.__omega0 = omega0
        self.__alpha = alpha
        self.__f = f
        self.__omega = omega

    def setTimings(self, tMax, tStep):
        self.__tMax = tMax
        self.__tStep = tStep

    def __diffEq(self, t, Y):
        # system of linked differential equations
        F = np.zeros(2)
        F[0] = Y[1]
        F[1] = -self.__omega0**2 * \
            np.sin(Y[0]) - self.__alpha*Y[1] + \
            self.__f * np.cos(self.__omega * t)
        return F

    def __RK4(self, t, Y, tStep):
        # Runge Kutta Methode
        k1 = tStep * self.__diffEq(t, Y)
        k2 = tStep * self.__diffEq(t + tStep/2, Y + k1/2)
        k3 = tStep * self.__diffEq(t + tStep/2, Y + k2/2)
        k4 = tStep * self.__diffEq(t + tStep, Y + k3)
        return Y + k1/6 + k2/3 + k3/3 + k4/6

    def __setTimeEvolution(self, initPos, initSpeed):
        self.__Y_0[0] = initPos
        self.__Y_0[1] = initSpeed

        self.timeSeq = np.zeros(int(self.__tMax/self.__tStep))
        self.positionSeq = np.zeros(int(self.__tMax/self.__tStep))
        self.speedSeq = np.zeros(int(self.__tMax/self.__tStep))

        Y = self.__Y_0
        for i in range(int(self.__tMax/self.__tStep)):
            t = i*self.__tStep
            Y = self.RK4(t, Y, self.__tStep)

            self.timeSeq[i] = t
            self.positionSeq[i] = Y[0]
            self.speedSeq[i] = Y[1]

    def timePlot(self, initPos, initSpeed):
        self.__setTimeEvolution(initPos, initSpeed)

        plt.plot(self.timeSeq, self.positionSeq)
        plt.xlabel("time in sec")
        plt.ylabel("position")
        plt.show()

    def phasePlot(self, initPos, initSpeed):
        self.__setTimeEvolution(initPos, initSpeed)

        plt.plot(self.posSeq, self.speedSeq)
        plt.xlabel("position")
        plt.ylabel("speed")
        plt.show()


class timeEvolutionPendulum(diffEqPendulum):
    tMax = 10

    self.setTimeEvolution(self.Y_0[0], self.Y_0[1])

    def setTimeEvolution(self, initPos, initSpeed):
        # calculate position and speed for all timesteps


class timeEvolutionSinForce(timeEvolutionPendulum):
    def diffEq(self, t, Y):
        # system of linked differential equations
        F = np.zeros(2)
        F[0] = Y[1]
        F[1] = -(self.omega0**2 + self.f * np.cos(self.omega * t)) * \
            np.sin(Y[0]) - self.alpha * Y[1]
        return F


class phaseSpacePendulum(timeEvolutionPendulum):
    noOfSequences = 100
    omega0 = 1
    h = 0.01
    tMax = 100
    xMax = 5
    yMax = 5
    timeSequences = np.zeros((100, 100))
    positionSequences = np.zeros((100, 100))
    speedSequences = np.zeros((100, 100))

    def __init__(self, alpha, f, omega, noOfSequences):
        self.alpha = alpha
        self.f = f
        self.omega = omega
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


class phaseSpaceSinForce(timeEvolutionSinForce, phaseSpacePendulum):
    # combine the two classes
    def __init__(self, alpha, f, omega, noOfSequences):
        phaseSpacePendulum.__init__(
            self, alpha, f, omega, noOfSequences)


class bifurcationPlotSinForce(phaseSpaceSinForce):
    f = rand.random()*2
    plotPoints = []

    def __init__(self):

        self.setBifurcationPlot()

    def setBifurcationPlot(self):
        for i in range(1, 5000):
            Y = np.zeros(2)
            Y[0] = 1
            Y[1] = 0
            self.f = rand.random()*2

            for j in range(int(self.tMax/self.h)):
                t = i*self.h
                Y = self.RK4(t, Y, self.h)

            oldPos = Y[0]

            while Y[0] / oldPos > 0:
                t = t + self.h/10
                Y = self.RK4(t, Y, self.h/10)
                np.append(self.plotPoints, (self.f, Y))

    def RK4(self, t, Y, h):
        # Runge Kutta Methode
        k1 = h * self.diffEq(t, Y)
        k2 = h * self.diffEq(t + h/2, Y + k1/2)
        k3 = h * self.diffEq(t + h/2, Y + k2/2)
        k4 = h * self.diffEq(t + h, Y + k3)
        return Y + k1/6 + k2/3 + k3/3 + k4/6


# =============================================================================

class exercises():
    message = "exercise:"

    def __init__(self):
        print(self.message)

    def e2a1(self):
        initPos = 0.1
        initSpeed = 0
        freePendulumSmallDisplacement = timeEvolutionPendulum(0, 0, 0)
        freePendulumSmallDisplacement.setTimeEvolution(initPos, initSpeed)
        freePendulumSmallDisplacement.timePlot()

    def e2a2(self):
        initPos = 1
        initSpeed = 0
        freePendulumLargeDisplacement = timeEvolutionPendulum(0, 0, 0)
        freePendulumLargeDisplacement.setTimeEvolution(initPos, initSpeed)
        freePendulumLargeDisplacement.timePlot()

    def e2a3(self):
        oneFreePendulum = phaseSpacePendulum(0, 0, 0, 1)
        oneFreePendulum.phasePlot()

    def e2b(self):
        noOfSequences = 100
        freePendulumPhaseSpace = phaseSpacePendulum(0, 0, 0, noOfSequences)
        freePendulumPhaseSpace.phasePlot()

    def e2c1(self):
        alpha = 0.1
        withFriction = timeEvolutionPendulum(alpha, 0, 0)
        withFriction.timePlot()

    def e2c2(self):
        alpha = 0.1
        noOfSequences = 100
        withFriction = phaseSpacePendulum(alpha, 0, 0, noOfSequences)
        withFriction.phasePlot()

    def e2d1(self):
        alpha = 0.1
        f = 0.2
        omega = 0.6
        frictionForce = timeEvolutionPendulum(alpha, f, omega)
        frictionForce.timePlot()

    def e2d2(self):
        alpha = 0.1
        f = 0.2
        omega = 0.6
        noOfSequences = 100
        frictionForce = phaseSpacePendulum(
            alpha, f, omega, noOfSequences)
        frictionForce.phasePlot()

    def e2d3(self):
        alpha = 0.1
        f = 0.8
        omega = 0.6
        frictionForce = timeEvolutionPendulum(alpha, f, omega)
        frictionForce.timePlot()

    def e2d4(self):
        alpha = 0.1
        f = 0.8
        omega = 0.6
        noOfSequences = 100
        frictionForce = phaseSpacePendulum(
            alpha, f, omega, noOfSequences)
        frictionForce.phasePlot()

    def e2e1(self):
        sinForce = phaseSpaceSinForce(0.1, 0.2, 2, 100)
        sinForce.phasePlot()

    def e2e2(self):
        biPlot = bifurcationPlotSinForce()

# ==============================================================================


exercise = exercises()

exercise.e2a1()
