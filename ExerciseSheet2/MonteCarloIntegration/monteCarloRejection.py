# %%
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x


class function:
    def f(self, x):
        return x


numOfPoints = 10000

x = np.arange(0, 1, 0.01)
y = f(x)

xRand = np.random.random(numOfPoints)
yRand = np.random.random(numOfPoints)

indicateBelowF = np.where(yRand < f(xRand))
indicateAboveF = np.where(yRand >= f(xRand))


plotPointsBelow = plt.scatter(
    xRand[indicateBelowF], yRand[indicateBelowF], color="green")
plotPointsAbove = plt.scatter(
    xRand[indicateAboveF], yRand[indicateAboveF], color="blue")
plt.plot(x, y, color="red")
plt.legend((plotPointsBelow, plotPointsAbove),
           ('Pts below the curve', 'Pts above the curve'),
           loc='lower left',
           ncol=3,
           fontsize=8)


# %%
