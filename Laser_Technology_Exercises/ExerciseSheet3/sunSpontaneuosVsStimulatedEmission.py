import numpy as np

# ==================================================================
# calculating ratio of spontaneous vs stimulated emission in the sum
# ==================================================================

# Constants
# ---------

# speed of light in vacuum:
c = 299792458  # m s*-1


# Calculation
# -----------

def p(T, f):

    # Boltzmann constant:
    kB = 1.38064852E-23  # m**2 kg s**-2 K**-1

    # Planck constant:
    h = 6.62607004E-34  # m**2 kg s**-1

    # probability
    p = 1/(np.exp((h * f) / (kB * T)) - 1)

    return p


# temperature
T = 5777

# wavelength
lambda_21 = 550E-9

# frequency
f_21 = c / lambda_21

# d_t n_stim / d_t n_spon
ratio = p(T, f_21)

print("The ratio of stimulated to spontaneous emission is: ", ratio)
