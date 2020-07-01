import random as rdm
import numpy as np


class species:
    N = 1000
    barriers = np.linspace(0, 1, N)  # species chain with barriers
    weakestSpecies = -1
    realTime = -1

    def __init__(self, N):
        # set size of species chain
        self.N = N
        self.barriers = np.linspace(0, 1, N)

        # assign a random barrier to each species
        for i in range(1, self.N):
            self.barriers[i - 1] = rdm.random()

        self.setWeakestSpecies()

    # find the species with the lowest barrier
    def setWeakestSpecies(self):
        min = 1
        for i in range(1, self.N):
            if self.barriers[i - 1] <= min:
                min = self.barriers[i - 1]
                self.weakestSpecies = i

    # set a new barrier for the species with the lowest barrier and the two surrounding species
    def mutate(self):
        self.setWeakestSpecies()

        # periodic boundary conditions
        if self.weakestSpecies == 1:
            self.barriers[self.N] = rdm.random()
            self.barriers[1] = rdm.random()
            self.barriers[2] = rdm.random()
        if self.weakestSpecies == self.N:
            self.barriers[self.N - 1] = rdm.random()
            self.barriers[self.N] = rdm.random()
            self.barriers[1] = rdm.random()

        else:
            self.barriers[self.weakestSpecies - 1] = rdm.random()
        self.barriers[self.weakestSpecies] = rdm.random()
        self.barriers[self.weakestSpecies + 1] = rdm.random()
        self.setWeakestSpecies()

    def setRealTime(self):
        self.realTime = 1


# =====================================

species1 = species(100)
print(species1.weakestSpecies)
species1.mutate()

