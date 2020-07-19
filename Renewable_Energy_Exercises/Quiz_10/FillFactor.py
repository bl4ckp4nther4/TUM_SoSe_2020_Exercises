import numpy as np


def fillFactor(U_oc, T):
    boltzmannConstant = 1.38064852e-23
    elementaryCharge = 1.60217662e-19

    x = elementaryCharge * U_oc / (boltzmannConstant * T)
    FF = (x - np.log(1 + x)) / (1 + x)

    return FF


print(fillFactor(0.6, 290))
print(fillFactor(0.6, 340))

