import numpy as np
import random
from matplotlib import pyplot as plt


N = 256

iterations = N**2

averageHeight = np.zeros(iterations)

# deposition sites
depSites = np.zeros(N)

for i in range(1, iterations):
    # random deposition location
    depLoc = int(np.floor(random.random() * N - 1))

    # neighboring particles can prevent holes from being filled
    if depSites[depLoc] < depSites[depLoc - 1] and depSites[depLoc] < depSites[depLoc + 1]:
        depSites[depLoc] = max((depSites[depLoc - 1], depSites[depLoc + 1]))
    else:
        depSites[depLoc] = depSites[depLoc] + 1

    averageHeight[i] = sum(depSites)/N

plt.plot(averageHeight, 'o', s=0.1)
plt.show()
