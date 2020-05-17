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
    __Y_0[0] = 0.1      # initial position
    __Y_0[1] = 0        # initial speed

    timeSeq = np.zeros(100)     # OUTPUT: time sequence
    posSeq = np.zeros(100)      # OUTPUT: position sequence
    speedSeq = np.zeros(100)    # OUTPUT: speed sequence

    __noOfSeqs = 100    # number of sequences calculated

    timeSeqs = np.zeros((100, 100))     # OUTPUT: time sequences
    posSeqs = np.zeros((100, 100))      # OUTPUT: position sequences
    speedSeqs = np.zeros((100, 100))    # OUTPUT: speed sequences

    __xMax = 5  # maximum absolute value of initial positions
    __vMax = 5  # maximum absolute value of initial speeds

    def __init__(self, omega0, alpha, f, omega):
        # constructing the differential equation
        self.__omega0 = omega0
        self.__alpha = alpha
        self.__f = f
        self.__omega = omega

    def __diffEq(self, t, Y):
        # system of linked differential equations

        F = np.zeros(2)

        F[0] = Y[1]
        F[1] = -self.__omega0**2 * \
            np.sin(Y[0]) - self.__alpha*Y[1] + \
            self.__f * np.cos(self.__omega * t)

        return F

    def __RK4(self, t, Y, tStep):
        # Runge Kutta Method for calculating the next timestep
        k1 = tStep * self.__diffEq(t, Y)
        k2 = tStep * self.__diffEq(t + tStep/2, Y + k1/2)
        k3 = tStep * self.__diffEq(t + tStep/2, Y + k2/2)
        k4 = tStep * self.__diffEq(t + tStep, Y + k3)
        return Y + k1/6 + k2/3 + k3/3 + k4/6

    def __setSeq(self, initPos, initSpeed):
        # calculating the position and speed for each timestep.

        # set the initial position and speed
        self.__Y_0[0] = initPos
        self.__Y_0[1] = initSpeed

        # reset and initialize sequence
        self.timeSeq = np.zeros(int(self.__tMax/self.__tStep))
        self.posSeq = np.zeros(int(self.__tMax/self.__tStep))
        self.speedSeq = np.zeros(int(self.__tMax/self.__tStep))

        # set first position and speed to initial position and speed
        Y = self.__Y_0
        for i in range(int(self.__tMax/self.__tStep)):
            # time
            t = i*self.__tStep

            # calculating the position and speed in the next timestep
            Y = self.__RK4(t, Y, self.__tStep)

            # save time, position and speed in arrays
            self.timeSeq[i] = t
            self.posSeq[i] = Y[0]
            self.speedSeq[i] = Y[1]

    def __setNSeqs(self, noOfSeqs):
        # calculaing N sequences and saving position and speed data of all

        # set the number of sequences
        self.__noOfSeqs = noOfSeqs

        # reset and initialize the sequences
        self.timeSeqs = np.zeros(
            (int(self.__tMax/self.__tStep), self.__noOfSeqs))
        self.posSeqs = np.zeros(
            (int(self.__tMax/self.__tStep), self.__noOfSeqs))
        self.speedSeqs = np.zeros(
            (int(self.__tMax/self.__tStep), self.__noOfSeqs))

        # initial position and speed, and sequence will be overwritten; save data in old* variables
        oldY_0 = self.__Y_0
        oldTimeSeq = self.timeSeq
        oldPosSeq = self.posSeq
        oldSpeedSeq = self.speedSeq

        for i in range(0, self.__noOfSeqs):
            # set random initial position and speed
            self.__Y_0[0] = rand.random() * 2*self.__xMax - self.__xMax
            self.__Y_0[1] = rand.random() * 2*self.__vMax - self.__vMax

            # calculate sequence
            self.__setSeq(self.__Y_0[0], self.__Y_0[1])

            # save sequence in 2D-Array
            self.timeSeqs[:, i] = self.timeSeq
            self.posSeqs[:, i] = self.posSeq
            self.speedSeqs[:, i] = self.speedSeq

        # reinstate the initial speed, position and whole sequence
        self.__Y_0 = oldY_0
        self.timeSeq = oldTimeSeq
        self.posSeq = oldPosSeq
        self.speedSeq = oldSpeedSeq

    def setTimings(self, tMax, tStep):
        # manually set custom time parameters
        self.__tMax = tMax
        self.__tStep = tStep

    def timePlot(self, initPos, initSpeed):
        # calculate one sequence and plot the position over time
        self.__setSeq(initPos, initSpeed)

        plt.plot(self.timeSeq, self.posSeq)
        plt.xlabel("time in sec")
        plt.ylabel("position")
        plt.show()

    def phasePlot(self, initPos, initSpeed):
        # calculate one sequence and plot the speed over the position
        self.__setSeq(initPos, initSpeed)

        plt.plot(self.posSeq, self.speedSeq)
        plt.xlabel("position")
        plt.ylabel("speed")
        plt.show()

    def setMaxPosSpeed(self, xMax, vMax):
        # set custom max position and speed values for the random initial values of the sequences
        self.__xMax = xMax
        self.__vMax = vMax

    def phasePlotSeqs(self, noOfSeqs):
        # calculate N sequences and plot the speed over the position
        self.__setNSeqs(noOfSeqs)

        plt.scatter(self.posSeqs, self.speedSeqs, s=0.05)
        plt.xlabel("position")
        plt.ylabel("speed")
        plt.show()


# class diffEqSinForce(diffEqPendulum):
#     def diffEq(self, t, Y):
#          # system of linked differential equations
#          F = np.zeros(2)
#          F[0] = Y[1]
#          F[1] = -(self.omega0**2 + self.f * np.cos(self.omega * t)) * \
#              np.sin(Y[0]) - self.alpha * Y[1]
#          return F


# class timeEvolutionSinForce(timeEvolutionPendulum):
#

# class phaseSpaceSinForce(timeEvolutionSinForce, phaseSpacePendulum):
#     # combine the two classes
#     def __init__(self, alpha, f, omega, noOfSequences):
#         phaseSpacePendulum.__init__(
#             self, alpha, f, omega, noOfSequences)


# class bifurcationPlotSinForce(phaseSpaceSinForce):
#     f = rand.random()*2
#     plotPoints = []

#     def __init__(self):

#         self.setBifurcationPlot()

#     def setBifurcationPlot(self):
#         for i in range(1, 5000):
#             Y = np.zeros(2)
#             Y[0] = 1
#             Y[1] = 0
#             self.f = rand.random()*2

#             for j in range(int(self.tMax/self.h)):
#                 t = i*self.h
#                 Y = self.RK4(t, Y, self.h)

#             oldPos = Y[0]

#             while Y[0] / oldPos > 0:
#                 t = t + self.h/10
#                 Y = self.RK4(t, Y, self.h/10)
#                 np.append(self.plotPoints, (self.f, Y))

#     def RK4(self, t, Y, h):
#         # Runge Kutta Methode
#         k1 = h * self.diffEq(t, Y)
#         k2 = h * self.diffEq(t + h/2, Y + k1/2)
#         k3 = h * self.diffEq(t + h/2, Y + k2/2)
#         k4 = h * self.diffEq(t + h, Y + k3)
#         return Y + k1/6 + k2/3 + k3/3 + k4/6


# =============================================================================

class exercises():
    message = "exercise:"

    def __init__(self):
        print(self.message)

    def e2a1(self):
        initPos = 0.1
        initSpeed = 0

        freePendSmallDisp = diffEqPendulum(1, 0, 0, 0)
        freePendSmallDisp.timePlot(initPos, initSpeed)

    def e2a2(self):
        initPos = 1
        initSpeed = 0

        freePendSmallDisp = diffEqPendulum(1, 0, 0, 0)
        freePendSmallDisp.timePlot(initPos, initSpeed)

    def e2a3(self):
        initPos = 1
        initSpeed = 0

        freePendSmallDisp = diffEqPendulum(1, 0, 0, 0)
        freePendSmallDisp.phasePlot(initPos, initSpeed)

    def e2b(self):
        noOfSequences = 100
        freePendulum = diffEqPendulum(1, 0, 0, 0)
        freePendulum.setTimings(100, 0.1)
        freePendulum.phasePlotSeqs(noOfSequences)

    def e2c1(self):
        alpha = 0.1
        withFriction = diffEqPendulum(1, alpha, 0, 0)
        withFriction.timePlot(1, 0)

    def e2c2(self):
        alpha = 0.1
        noOfSequences = 100
        withFriction = diffEqPendulum(1, alpha, 0, 0)
        withFriction.setTimings(100, 0.1)
        withFriction.phasePlotSeqs(noOfSequences)

    def e2d1(self):
        alpha = 0.1
        f = 0.2
        omega = 0.6
        frictionForce = diffEqPendulum(1, alpha, f, omega)
        frictionForce.setTimings(100, 0.1)
        frictionForce.timePlot(1, 0)

    def e2d2(self):
        alpha = 0.1
        f = 0.2
        omega = 0.6
        noOfSequences = 100
        frictionForce = diffEqPendulum(1, alpha, f, omega)
        frictionForce.setTimings(100, 0.01)
        frictionForce.phasePlotSeqs(noOfSequences)

    def e2d3(self):
        alpha = 0.1
        f = 0.8
        omega = 0.6
        frictionForce = diffEqPendulum(1, alpha, f, omega)
        frictionForce.setTimings(100, 0.1)
        frictionForce.timePlot(1, 0)

    def e2d4(self):
        alpha = 0.1
        f = 0.8
        omega = 0.6
        noOfSequences = 100
        frictionForce = diffEqPendulum(1, alpha, f, omega)
        frictionForce.setTimings(100, 0.01)
        frictionForce.phasePlotSeqs(noOfSequences)

    # def e2e1(self):
    #     sinForce = phaseSpaceSinForce(0.1, 0.2, 2, 100)
    #     sinForce.phasePlot()

    # def e2e2(self):
    #     biPlot = bifurcationPlotSinForce()

# ==============================================================================


exercise = exercises()

exercise.e2d4()
