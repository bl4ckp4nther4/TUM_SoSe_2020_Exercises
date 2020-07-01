import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys


class wavePacketDoubleSlit:

    # discretization of the space domain
    N_x = 100  # number of sections in space (number of points = N+1)
    xStart = 0  # left border of space
    xEnd = 10  # right border of space
    d_x = (xEnd - xStart) / N_x  # size of one section in space
    d_y = d_x
    x = np.linspace(xStart, xEnd, N_x + 1)[np.newaxis]
    y = np.transpose(x)

    # discretization of the time domain
    N_t = 100
    d_t = (d_x / 2) ** 2  # timesteps
    T = d_t * N_t  # total time

    # properties of the wave packet
    x_0 = (xEnd - xStart) / 2  # starting point of the wavepacket
    y_0 = x_0
    sigma_0 = (xEnd - xStart) / 10  # width of wave packet in space
    k_0 = 32 * np.pi  # speed of the wave packet

    # initial wave packet
    gauss2d = np.exp(-1 / 2 * (x - x_0) ** 2 / (sigma_0) ** 2) * np.exp(
        -1 / 2 * (y - y_0) ** 2 / (sigma_0) ** 2
    )
    realInitWF = gauss2d * np.cos(k_0 * x)
    imagInitWF = gauss2d * np.sin(k_0 * x)

    slitWidth = 1
    slitDist = 3

    probDensity = []
    interferencePattern = []

    def __init__(self, N_x, xEnd, N_t, x_0, sigma_0, slitWidth, slitDist):
        self.N_x = N_x
        self.xEnd = xEnd
        self.d_x = (self.xEnd - self.xStart) / self.N_x  # size of one section in space
        self.probDensity = np.zeros([self.N_x + 1, self.N_x + 1, self.N_t + 1])
        self.x = np.linspace(self.xStart, self.xEnd, self.N_x + 1)[np.newaxis]
        self.y = np.transpose(self.x)

        self.N_t = N_t
        self.d_t = (self.d_x / 2) ** 2  # timesteps
        self.T = self.d_t * self.N_t  # total time

        self.x_0 = x_0
        self.sigma_0 = sigma_0
        self.gauss2d = np.exp(
            -1 / 2 * (self.x - self.x_0) ** 2 / (self.sigma_0) ** 2
        ) * np.exp(-1 / 2 * (self.y - self.y_0) ** 2 / (self.sigma_0) ** 2)
        self.realInitWF = self.gauss2d * np.cos(self.k_0 * self.x)
        self.imagInitWF = self.gauss2d * np.sin(self.k_0 * self.x)

        self.slitWidth = slitWidth
        self.slitDist = slitDist

        self.probDensity = self.setTimeEvolution(
            self.N_x,
            self.d_x,
            self.d_y,
            self.N_t,
            self.d_t,
            self.realInitWF,
            self.imagInitWF,
            self.slitWidth,
            self.slitDist,
        )

    def setTimeEvolution(
        self, N_x, d_x, d_y, N_t, d_t, realInitWF, imagInitWF, slitWidth, slitDist
    ):

        # points to set up the double slits
        A = N_x / 2 - (slitDist - 1) / 2 - slitWidth
        B = N_x / 2 - (slitDist - 1) / 2
        C = N_x / 2 + (slitDist - 1) / 2 + 1
        D = N_x / 2 + (slitDist - 1) / 2 + slitWidth + 1

        pot = np.zeros([N_x + 1, N_x + 1])  # potential is zero everywhere

        # initializing the 2D arrays for real part imag part and prob density
        realWF = np.zeros([N_x + 1, N_x + 1, N_t + 1])
        imagWF = np.zeros([N_x + 1, N_x + 1, N_t + 1])
        probDensity = np.zeros([N_x + 1, N_x + 1, N_t + 1])
        self.interferencePattern = np.zeros((N_x + 1, N_t + 1))

        # setting the first timestep to the initial wave function
        realWF[:, :, 0] = realInitWF
        imagWF[:, :, 0] = imagInitWF

        # going through all time steps
        for n in range(0, N_t):
            if n % 10 == 0:
                percent = 100 * n / N_t
                sys.stdout.flush()
                sys.stdout.write("\r{0}>".format("=" * int(percent)))
                sys.stdout.write("\r{0}>".format("-" * int(100 - percent)))

            # going through all positions for the real part
            for i in range(0, N_x):
                for j in range(0, N_x):

                    # setting the slit to 0
                    realWF[0 : int(A), int(N_x / 2), n + 1] = 0
                    realWF[int(B) : int(C), int(N_x / 2), n + 1] = 0
                    realWF[int(D) : N_x, int(N_x / 2), n + 1] = 0

                    # setting the real part of the wavefunction according to the lecture
                    realWF[i, j, n + 1] = (
                        realWF[i, j, n]
                        + (2 * d_t / d_x ** 2 + 2 * d_t / d_y ** 2 + d_t * pot[i, j])
                        * imagWF[i, j, n]
                        - d_t / d_x ** 2 * (imagWF[i + 1, j, n] + imagWF[i - 1, j, n])
                        - d_t / d_y ** 2 * (imagWF[i, j + 1, n] + imagWF[i, j - 1, n])
                    )

            # setting the slit to 0
            realWF[0 : int(A), int(N_x / 2), :] = 0
            realWF[int(B) : int(C), int(N_x / 2), :] = 0
            realWF[int(D) : N_x, int(N_x / 2), :] = 0

            # going through all positions for the imaginary part
            for i in range(1, N_x - 1):
                for j in range(1, N_x - 1):

                    # setting the slit to 0
                    imagWF[0 : int(A), int(N_x / 2), n + 1] = 0
                    imagWF[int(B) : int(C), int(N_x / 2), n + 1] = 0
                    imagWF[int(D) : N_x, int(N_x / 2), n + 1] = 0

                    # setting the imaginary part of the wavefunction according to the lecture
                    imagWF[i, j, n + 1] = (
                        imagWF[i, j, n]
                        - (2 * d_t / d_x ** 2 + 2 * d_t / d_y ** 2 + d_t * pot[i, j])
                        * realWF[i, j, n + 1]
                        + d_t
                        / d_x ** 2
                        * (realWF[i + 1, j, n + 1] + realWF[i - 1, j, n + 1])
                        + d_t
                        / d_y ** 2
                        * (realWF[i, j + 1, n + 1] + realWF[i, j - 1, n + 1])
                    )

                # setting the slit to 0
                imagWF[0 : int(A), int(N_x / 2), :] = 0
                imagWF[int(B) : int(C), int(N_x / 2), :] = 0
                imagWF[int(D) : N_x, int(N_x / 2), :] = 0

            # setting the probability density after calculating each time step
            probDensity[:, :, n + 1] = (
                realWF[:, :, n + 1] ** 2 + imagWF[:, :, n] * imagWF[:, :, n + 1]
            )
            self.interferencePattern[:, n + 1] = probDensity[:, 0, n + 1]
        return probDensity


N_x = 128
N_t = 512

xEnd = 10
x_0 = 6
sigma_0 = 0.5

# calculation of the probability density
probDensitySlits = wavePacketDoubleSlit(N_x, xEnd, N_t, x_0, sigma_0, 2, 11)

probDensity = probDensitySlits.probDensity
x = probDensitySlits.x
y = probDensitySlits.y
interferencePattern = probDensitySlits.interferencePattern

plt.imshow(
    interferencePattern, interpolation="nearest", cmap=cm.gist_rainbow,
)
plt.show()

# 2d plot prob density
nrows, ncols = N_x + 1, N_x + 1
for n in range(0, N_t):
    if n % 10 == 0:
        print("t = ", n)
        plt.imshow(
            probDensity[:, :, n],
            extent=(x.min(), x.max(), y.max(), y.min()),
            interpolation="nearest",
        )
        plt.show()

