import numpy as np
import matplotlib.pyplot as plt
import random as rand


class diffEqPendulum():
    _omega0 = 1  # angular frequency of the pendulum for small angles
    _alpha = 0   # friction
    _f = 0       # driving force
    _omega = 0   # frequency of the driving force

    _tMax = 10       # total time length
    _tStep = 0.1     # length of one time step

    _Y_0 = np.zeros(2)  # vector Y
    _Y_0[0] = 0.1      # initial position
    _Y_0[1] = 0        # initial speed

    timeSeq = np.zeros(100)     # OUTPUT: time sequence
    posSeq = np.zeros(100)      # OUTPUT: position sequence
    speedSeq = np.zeros(100)    # OUTPUT: speed sequence

    _noOfSeqs = 100    # number of sequences calculated

    timeSeqs = np.zeros((100, 100))     # OUTPUT: time sequences
    posSeqs = np.zeros((100, 100))      # OUTPUT: position sequences
    speedSeqs = np.zeros((100, 100))    # OUTPUT: speed sequences

    _xMax = 5  # maximum absolute value of initial positions
    _vMax = 5  # maximum absolute value of initial speeds

    def __init__(self, omega0, alpha, f, omega):
        # constructing the differential equation
        self._omega0 = omega0
        self._alpha = alpha
        self._f = f
        self._omega = omega

    def _diffEq(self, t, Y):
        # system of linked differential equations

        F = np.zeros(2)

        F[0] = Y[1]
        F[1] = -self._omega0**2 * \
            np.sin(Y[0]) - self._alpha*Y[1] + \
            self._f * np.cos(self._omega * t)

        return F

    def _RK4(self, t, Y, tStep):
        # Runge Kutta Method for calculating the next timestep
        k1 = tStep * self._diffEq(t, Y)
        k2 = tStep * self._diffEq(t + tStep/2, Y + k1/2)
        k3 = tStep * self._diffEq(t + tStep/2, Y + k2/2)
        k4 = tStep * self._diffEq(t + tStep, Y + k3)
        return Y + k1/6 + k2/3 + k3/3 + k4/6

    def _setSeq(self, initPos, initSpeed):
        # calculating the position and speed for each timestep.

        # set the initial position and speed
        self._Y_0[0] = initPos
        self._Y_0[1] = initSpeed

        # reset and initialize sequence
        self.timeSeq = np.zeros(int(self._tMax/self._tStep))
        self.posSeq = np.zeros(int(self._tMax/self._tStep))
        self.speedSeq = np.zeros(int(self._tMax/self._tStep))

        # set first position and speed to initial position and speed
        Y = self._Y_0
        for i in range(int(self._tMax/self._tStep)):
            # time
            t = i*self._tStep

            # calculating the position and speed in the next timestep
            Y = self._RK4(t, Y, self._tStep)

            # save time, position and speed in arrays
            self.timeSeq[i] = t
            self.posSeq[i] = Y[0]
            self.speedSeq[i] = Y[1]

    def _setNSeqs(self, noOfSeqs):
        # calculaing N sequences and saving position and speed data of all

        # set the number of sequences
        self._noOfSeqs = noOfSeqs

        # reset and initialize the sequences
        self.timeSeqs = np.zeros(
            (int(self._tMax/self._tStep), self._noOfSeqs))
        self.posSeqs = np.zeros(
            (int(self._tMax/self._tStep), self._noOfSeqs))
        self.speedSeqs = np.zeros(
            (int(self._tMax/self._tStep), self._noOfSeqs))

        # initial position and speed, and sequence will be overwritten; save data in old* variables
        oldY_0 = self._Y_0
        oldTimeSeq = self.timeSeq
        oldPosSeq = self.posSeq
        oldSpeedSeq = self.speedSeq

        for i in range(0, self._noOfSeqs):
            # set random initial position and speed
            self._Y_0[0] = rand.random() * 2*self._xMax - self._xMax
            self._Y_0[1] = rand.random() * 2*self._vMax - self._vMax

            # calculate sequence
            self._setSeq(self._Y_0[0], self._Y_0[1])

            # save sequence in 2D-Array
            self.timeSeqs[:, i] = self.timeSeq
            self.posSeqs[:, i] = self.posSeq
            self.speedSeqs[:, i] = self.speedSeq

        # reinstate the initial speed, position and whole sequence
        self._Y_0 = oldY_0
        self.timeSeq = oldTimeSeq
        self.posSeq = oldPosSeq
        self.speedSeq = oldSpeedSeq

    def setTimings(self, tMax, tStep):
        # manually set custom time parameters
        self._tMax = tMax
        self._tStep = tStep

    def timePlot(self, initPos, initSpeed):
        # calculate one sequence and plot the position over time
        self._setSeq(initPos, initSpeed)

        plt.plot(self.timeSeq, self.posSeq)
        plt.xlabel("time in sec")
        plt.ylabel("position")
        plt.show()

    def phasePlot(self, initPos, initSpeed):
        # calculate one sequence and plot the speed over the position
        self._setSeq(initPos, initSpeed)

        plt.plot(self.posSeq, self.speedSeq)
        plt.xlabel("position")
        plt.ylabel("speed")
        plt.show()

    def setMaxPosSpeed(self, xMax, vMax):
        # set custom max position and speed values for the random initial values of the sequences
        self._xMax = xMax
        self._vMax = vMax

    def phasePlotSeqs(self, noOfSeqs):
        # calculate N sequences and plot the speed over the position
        self._setNSeqs(noOfSeqs)

        plt.scatter(self.posSeqs, self.speedSeqs, s=0.05)
        plt.xlabel("position")
        plt.ylabel("speed")
        plt.show()


class diffEqSinForce(diffEqPendulum):
    # OUTPUT: data for the bifurcation plot
    bifurcationData = np.zeros((1, 3))
    bifurcationDataTimeOut = np.zeros((1, 3))
    trajectoryEnd = []
    timeOut = False

    def _diffEq(self, t, Y):
        # system of linked differential equations

        F = np.zeros(2)

        F[0] = Y[1]
        F[1] = -(self._omega0**2 + self._f * np.cos(self._omega * t)) * \
            np.sin(Y[0]) - self._alpha * Y[1]

        return F

    def plotBifurcationData(self, noOfSeqs):

        for i in range(1, noOfSeqs):  # till 5000
            print(i)
            Y = np.zeros(2)

            # initial conditions
            Y[0] = 1
            Y[1] = 0
            # random magnitide of the driving force
            self._f = rand.random()*2

            # calculating the trajectory of the pendulum until tMax
            for j in range(int(self._tMax/self._tStep)):
                t = j*self._tStep
                Y = self._RK4(t, Y, self._tStep)

            oldPos = Y[0]
            # calculating the trajectory until the position is at 0
            while Y[0] / oldPos > 0:
                oldPos = Y[0]

                # time steps 10 times smaller
                t = t + self._tStep/10
                if t > 1.2*self._tMax:
                    self.timeOut = True
                    break

                Y = self._RK4(t, Y, self._tStep/10)
                self.trajectoryEnd = np.append(self.trajectoryEnd, Y[0])

            # set bifuricationData
            if self.timeOut == True:
                self.bifurcationDataTimeOut = np.append(
                    self.bifurcationDataTimeOut, [[self._f, np.abs(Y[0]), np.abs(Y[1])]], axis=0)
            else:
                self.bifurcationData = np.append(
                    self.bifurcationData, [[self._f, np.abs(Y[0]), np.abs(Y[1])]], axis=0)

        plt.scatter(self.bifurcationData[:, 0], self.bifurcationData[:, 2])
        plt.scatter(
            self.bifurcationDataTimeOut[:, 0], self.bifurcationDataTimeOut[:, 2])
        plt.show()

    def _setNSeqsRandf(self, noOfSeqs):
        # calculaing N sequences and saving position and speed data of all

        self._Y_0[0] = 1
        self._Y_0[1] = 0
        # set the number of sequences
        self._noOfSeqs = noOfSeqs

        # reset and initialize the sequences
        self.timeSeqs = np.zeros(
            (int(self._tMax/self._tStep), self._noOfSeqs))
        self.posSeqs = np.zeros(
            (int(self._tMax/self._tStep), self._noOfSeqs))
        self.speedSeqs = np.zeros(
            (int(self._tMax/self._tStep), self._noOfSeqs))

        # initial f and sequence will be overwritten; save data in old* variables
        oldf = self._f
        oldTimeSeq = self.timeSeq
        oldPosSeq = self.posSeq
        oldSpeedSeq = self.speedSeq

        for i in range(0, self._noOfSeqs):
            # set random initial position and speed
            self._f = rand.random() * 2
            # calculate sequence
            self._setSeq(self._Y_0[0], self._Y_0[1])

            # save sequence in 2D-Array
            self.timeSeqs[:, i] = self.timeSeq
            self.posSeqs[:, i] = self.posSeq
            self.speedSeqs[:, i] = self.speedSeq

        # reinstate the force and whole sequence
        self._f = oldf
        self.timeSeq = oldTimeSeq
        self.posSeq = oldPosSeq
        self.speedSeq = oldSpeedSeq

    def phasePlotSeqsRandf(self, noOfSeqs):
        # calculate N sequences and plot the speed over the position
        self._setNSeqsRandf(noOfSeqs)

        plt.scatter(self.posSeqs, self.speedSeqs, s=0.05)
        plt.xlabel("position")
        plt.ylabel("speed")
        plt.show()

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

    def e2e1(self):
        sinForce = diffEqSinForce(1, 0.1, 0.2, 2)
        sinForce.setTimings(200, 0.1)
        sinForce.timePlot(0.1, 0)

    def e2e2(self):
        sinForce = diffEqSinForce(1, 0.1, 0.2, 2)
        sinForce.setTimings(200, 0.1)
        sinForce.phasePlot(0.1, 0)

    def e2e3(self):
        sinForce = diffEqSinForce(1, 0.1, 0.2, 2)
        sinForce.setTimings(200, 0.1)
        sinForce.phasePlotSeqs(100)

    def e2e4(self):
        sinForce = diffEqSinForce(1, 0.1, 0.2, 2)
        sinForce.setTimings(200, 0.1)
        sinForce.plotBifurcationData(250)

# ==============================================================================


exercise = exercises()

exercise.e2e4()
