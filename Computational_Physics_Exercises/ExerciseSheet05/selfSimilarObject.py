import numpy as np
import random
from matplotlib import pyplot as plt

N = 10000

allPoints = np.zeros((N, 2))

x = 0.5
y = 0

for i in range(1, N):
    # select one the replacement procedures randomly
    r = random.random()

    # replacement procedures
    if r >= 0 and r < 0.1:
        x = 0.1 * x
        y = 0.6 * y
    elif r >= 0.1 and r < 0.2:
        x = 0.05 * x
        y = -0.5 * y + 1
    elif r >= 0.2 and r < 0.4:
        x = 0.46*x - 0.15*y
        y = 0.39*x + 0.38*y + 0.6
    elif r >= 0.4 and r < 0.6:
        x = 0.74*x - 0.15*y
        y = 0.17*x + 0.42*y + 1.1
    elif r >= 0.6 and r < 0.8:
        x = 0.43*x + 0.28*y
        y = -0.25*x + 0.45*y + 1
    elif r >= 0.8 and r <= 1:
        x = 0.42*x + 0.26*y
        y = 0.35*x + 0.31*y + 0.7

    # save point in array
    allPoints[i, :] = (x, y)

print(allPoints)
plt.scatter(allPoints[:, 0], allPoints[:, 1], s=1)
plt.show()
