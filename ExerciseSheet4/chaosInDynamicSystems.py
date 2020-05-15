import numpy as np
import matplotlib.pyplot as plt


Y = [0.1, 1]

omega0 = 1
alpha = 0
f = 0
omega = 0
h = 0.1

Y_1 = 0.1
Y_2 = 0

Y = np.array([Y_1, Y_2])


def F(t, Y):
    F_1 = Y[1]
    F_2 = -omega0**2 * np.sin(Y[0]) - alpha*Y[1] + f * np.cos(omega * t)
    return np.array([F_1, F_2])


def RK4(Y, t, h):
    k1 = h * F(t, Y)
    k2 = h * F(t + h/2, Y + k1/2)
    k3 = h * F(t + h/2, Y + k2/2)
    k4 = h * F(t + h, Y + k3)
    return Y + k1/2 + k2/3 + k3/3 + k4/6


points = np.zeros((int(10/h), 2))

for i in range(int(10/h)):
    t = i*h
    print(t)
    Y = RK4(Y, t, h)
    points[i, 0] = t
    points[i, 1] = Y[0]

plt.plot(points[:, 0], points[:, 1])
plt.show()

