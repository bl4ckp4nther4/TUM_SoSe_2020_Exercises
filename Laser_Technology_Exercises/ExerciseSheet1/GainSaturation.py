import numpy as np
import matplotlib.pyplot as plt


def powerOut(R):
    smallSignalGain = 100
    saturationPower = 2E-3  # Watts

    powerOut = saturationPower*(1 - R)*(smallSignalGain * R - 1)
    return powerOut


R = np.linspace(0, 1, 1000)

powerOutVec = powerOut(R)

plt.plot(R, powerOutVec)
plt.xlabel("R")
plt.ylabel("Power out in Watts")

plt.show()
