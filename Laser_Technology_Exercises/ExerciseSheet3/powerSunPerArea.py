import numpy as np

# ======================================================
# calculating the emitted power of the sun per unit area
# ======================================================

# Constants
# ---------

# Boltzmann constant:
kB = 1.38064852E-23  # m**2 kg s**-2 K**-1

# speed of light in vacuum:
c = 299792458  # m s*-1

# Planck constant:
h = 6.62607004E-34  # m**2 kg s**-1

# Stefan-Boltzmann constant:
sigma = 2/15 * np.pi**5 * kB**4 / (c**2 * h**3)

print("sigma = ", sigma, "watts / (m^2 K^4)")

# Calculation
# -----------

# temperature of the sun:
T = 5777  # kelvin

# emitted power per unit area:
I = sigma * T**4  # watt m**-2

print("The emitted power per unit area from the sun is ",
      I, "watts per meter squared.")
