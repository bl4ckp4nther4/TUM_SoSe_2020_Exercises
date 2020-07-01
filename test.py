import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys

N_x = 128


slitWidth = 1
slitDist = 1

realWF = np.ones((N_x + 1, N_x + 1))

realWF[0, :] = 0
realWF[N_x, :] = 0
realWF[:, 0] = 0
realWF[:, N_x] = 0

A = N_x / 2 - (slitDist - 1) / 2 - slitWidth
B = N_x / 2 - (slitDist - 1) / 2
C = N_x / 2 + (slitDist - 1) / 2 + 1
D = N_x / 2 + (slitDist - 1) / 2 + slitWidth + 1

realWF[0 : int(A), int(N_x / 2)] = 0
realWF[int(B) : int(C), int(N_x / 2),] = 0
realWF[int(D) : N_x, int(N_x / 2)] = 0


# 2d plot prob density
nrows, ncols = N_x + 1, N_x + 1
plt.imshow(
    realWF[:, :], interpolation="nearest", cmap=cm.gist_rainbow,
)
plt.show()
