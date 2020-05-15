import numpy as np
import matplotlib.pyplot as plt


class freePendulumDiffEq():
    omega0 = 1  # angular frequency of the pendulum for small angles
    alpha = 0   # starting angle
    f = 0       # driving force
    omega = 0   # angular frequency of the driving force
    h = 0.1     # length of one time step

    Y = np.zeros(2)  # vector Y
    Y[0] = 0.1  # initial position
    Y[1] = 0   # initial speed

    def __init__(self, omega0):
        self.omega0 = omega0
        self.alpha = 0
        self.f = 0
        self.Y = np.zeros(2)  # vector Y
        self.Y[0] = 0.1  # initial position
        self.Y[1] = 0   # initial speed

    def diffEq(self, t, Y):
        # system of linked differential equations
        F = np.zeros(2)
        F[0] = Y[1]
        F[1] = -self.omega0**2 * \
            np.sin(Y[0]) - self.alpha*Y[1] + self.f * np.cos(self.omega * t)
        return F


class timeEvolutionFreePendulum(freePendulumDiffEq):
    tMax = 10
    h = freePendulumDiffEq.h
    timeEvolution = np.zeros((int(tMax/h), 2))

    def __init__(self, omega0, tMax):
        self.omega0 = omega0
        self.alpha = 0
        self.f = 0
        self.Y = np.zeros(2)  # vector Y
        self.Y[0] = 0.1  # initial position
        self.Y[1] = 0   # initial speed

        self.tMax = tMax

        self.setTimeEvolution()

    def RK4(self, t, Y):
        # Runge Kutta Methode
        k1 = self.h * self.diffEq(t, Y)
        k2 = self.h * self.diffEq(t + self.h/2, Y + k1/2)
        k3 = self.h * self.diffEq(t + self.h/2, Y + k2/2)
        k4 = self.h * self.diffEq(t + self.h, Y + k3)
        return Y + k1/2 + k2/3 + k3/3 + k4/6

    def setTimeEvolution(self):
        # calculate position and speed for all timesteps

        self.timeEvolution = np.zeros((int(self.tMax/self.h), 2))
        Y = self.Y
        for i in range(int(self.tMax/self.h)):
            t = i*self.h
            Y = self.RK4(t, Y)

            self.timeEvolution[i, 0] = t
            self.timeEvolution[i, 1] = Y[0]


exercise1a1 = timeEvolutionFreePendulum(1, 10)
plt.plot(exercise1a1.timeEvolution[:, 0], exercise1a1.timeEvolution[:, 1])
plt.show()
