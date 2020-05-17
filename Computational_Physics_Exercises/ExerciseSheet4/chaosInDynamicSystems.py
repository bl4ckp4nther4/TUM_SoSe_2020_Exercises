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

    def __init__(self):
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

    def __init__(self, alpha):
        self.alpha = alpha

        timeEvolutionFreePendulum.__init__(self)


class timeEvolutionFrictionAndForce(timeEvolutionFrictionPendulum):
    f = 1
    omega = 2
    tMax = 100

    def __init__(self, alpha, f, omega):
        self.f = f
        self.omega = omega
        timeEvolutionFrictionPendulum.__init__(self, alpha, )


class timeEvolutionSinForce(timeEvolutionFrictionAndForce):
    def diffEq(self, t, Y):
        # system of linked differential equations
        F = np.zeros(2)
        F[0] = Y[1]
        F[1] = -(self.omega0**2 + self.f * np.cos(self.omega * t)) * \
            np.sin(Y[0]) - self.alpha * Y[1]
        return F


class phaseSpaceFreePendulum(timeEvolutionFreePendulum):
    noOfSequences = 100
    omega0 = 1
    h = 0.01
    tMax = 100
    xMax = 5
    yMax = 5
    timeSequences = np.zeros((100, 100))
    positionSequences = np.zeros((100, 100))
    speedSequences = np.zeros((100, 100))

    def __init__(self, noOfSequences):
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

    def __init__(self, alpha, noOfSequences):
        self.alpha = alpha
        phaseSpaceFreePendulum.__init__(self, noOfSequences)


class phaseSpaceFrictionAndForce(phaseSpaceFrictionPendulum):
    f = 1
    omega = 2

    def __init__(self, alpha, f, omega, noOfSequences):
        self.f = f
        self.omega = omega
        phaseSpaceFrictionPendulum.__init__(self, alpha, noOfSequences)


class phaseSpaceSinForce(timeEvolutionSinForce, phaseSpaceFrictionAndForce):
    # combine the two classes
    def __init__(self, alpha, f, omega, noOfSequences):
        phaseSpaceFrictionAndForce.__init__(
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

    def __init__(self):
        print("exercise:")

    def e2a1():
        initPos = 0.1
        initSpeed = 0
        freePendulumSmallDisplacement = timeEvolutionFreePendulum()
        freePendulumSmallDisplacement.setTimeEvolution(initPos, initSpeed)
        freePendulumSmallDisplacement.timePlot()

    def e2a2():
        initPos = 1
        initSpeed = 0
        freePendulumLargeDisplacement = timeEvolutionFreePendulum()
        freePendulumLargeDisplacement.setTimeEvolution(initPos, initSpeed)
        freePendulumLargeDisplacement.timePlot()

    def e2a3():
        oneFreePendulum = phaseSpaceFreePendulum(1)
        oneFreePendulum.phasePlot()

    def e2b():
        noOfSequences = 100
        freePendulumPhaseSpace = phaseSpaceFreePendulum(noOfSequences)
        freePendulumPhaseSpace.phasePlot()

    def e2c1():
        alpha = 0.1
        withFriction = timeEvolutionFrictionPendulum(alpha)
        withFriction.timePlot()

    def e2c2():
        alpha = 0.1
        noOfSequences = 100
        withFriction = phaseSpaceFrictionPendulum(alpha, noOfSequences)
        withFriction.phasePlot()

    def e2d1():
        alpha = 0.1
        f = 0.2
        omega = 0.6
        frictionForce = timeEvolutionFrictionAndForce(alpha, f, omega)
        frictionForce.timePlot()

    def e2d2():
        alpha = 0.1
        f = 0.2
        omega = 0.6
        noOfSequences = 100
        frictionForce = phaseSpaceFrictionAndForce(
            alpha, f, omega, noOfSequences)
        frictionForce.phasePlot()

    def e2d3():
        alpha = 0.1
        f = 0.8
        omega = 0.6
        frictionForce = timeEvolutionFrictionAndForce(alpha, f, omega)
        frictionForce.timePlot()

    def e2d4():
        alpha = 0.1
        f = 0.8
        omega = 0.6
        noOfSequences = 100
        frictionForce = phaseSpaceFrictionAndForce(
            alpha, f, omega, noOfSequences)
        frictionForce.phasePlot()

    def e2e1():
        sinForce = phaseSpaceSinForce(0.1, 0.2, 2, 100)
        sinForce.phasePlot()

    def e2e2():
        biPlot = bifurcationPlotSinForce()

# ==============================================================================


exercises.e2a2()
