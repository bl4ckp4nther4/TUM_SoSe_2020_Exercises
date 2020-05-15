import numpy as np

# Constants
planckConstant = 6.62607004E-34  # m^2 * kg / s
speedOfLight = 299792458         # meters / second

# Parameters
length = 1E-3        # meters
waveLength = 670E-9  # meters
powerOut = 5E-3      # watt
refractiveIndex = 3.3

# Equations
reflectionCoefficient = (refractiveIndex - 1) ** 2/(refractiveIndex + 1) ** 2

# 1a)
# Number of photons per second:
photonEnergy = planckConstant*speedOfLight/waveLength
numberOfPhotonsOut = powerOut/photonEnergy
print("Number of photons out: ", numberOfPhotonsOut, " / second")

# 1b)
# Number of photons in the cavity
timePerRoundTrip = 2*length*refractiveIndex/speedOfLight
power = powerOut/(1-reflectionCoefficient)

energyInCavity = timePerRoundTrip*power
numberOfPhotonsInCavity = energyInCavity/photonEnergy
print("Number of photons in cavity: ", numberOfPhotonsInCavity)
