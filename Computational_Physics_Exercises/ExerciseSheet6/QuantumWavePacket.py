import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def SL(realInitialWave, imagInitialWave, potential, delta_x, N, delta_t, T):
    # calculating the probability density of of all timesteps and points in space

    # initializing the 2D arrays for real part imag part and prob density
    realWaveFkt = np.zeros([N + 1, int(T / delta_t + 1)])
    imagWaveFkt = np.zeros([N + 1, int(T / delta_t + 1)])
    probDensity = np.zeros([N + 1, int(T / delta_t + 1)])

    # setting the first timestep to the initial wave function
    realWaveFkt[:, 0] = realInitialWave
    imagWaveFkt[:, 0] = imagInitialWave

    # going through all time steps
    for n in range(0, int(np.ceil(T / delta_t) - 1)):

        # setting the borders to 0
        realWaveFkt[0, n + 1] = 0
        realWaveFkt[N, n + 1] = 0
        imagWaveFkt[0, n + 1] = 0
        imagWaveFkt[N, n + 1] = 0

        # goint through all positions
        for i in range(1, N - 1):

            # setting the real part of the wavefunction according to the lecture
            realWaveFkt[i, n + 1] = (
                realWaveFkt[i, n]
                + (2 * delta_t / delta_x ** 2 + potential[i] * delta_t)
                * imagWaveFkt[i, n]
                - delta_t
                / delta_x ** 2
                * (imagWaveFkt[i + 1, n] + imagWaveFkt[i - 1, n])
            )
            # setting the imaginary part of the wavefunction according to the lecture
            imagWaveFkt[i, n + 1] = (
                imagWaveFkt[i, n]
                - (2 * delta_t / delta_x ** 2 + potential[i] * delta_t)
                * realWaveFkt[i, n + 1]
                + delta_t
                / delta_x ** 2
                * (realWaveFkt[i + 1, n + 1] + realWaveFkt[i - 1, n + 1])
            )

        # setting the probability density after calculating each time step
        probDensity[:, n + 1] = (
            realWaveFkt[:, n + 1] ** 2 + imagWaveFkt[:, n] * imagWaveFkt[:, n + 1]
        )

    return probDensity


sigma_0 = 0.5  # width of wavepacket in space
k_0 = 17 * np.pi  # k_0 = 0
delta_x = 0.01
x_0 = 2.5  # starting

start = 0  # left border of space
end = 5  # right border of space
N = 200  # number of sections in space (number of points = N+1)
delta_x = (end - start) / N  # size of one section in space
x = np.linspace(start, end, N + 1)

delta_t = (delta_x / 2) ** 2  # timesteps
T = delta_t * 100  # total time

# initial wavepacket in real and imaginary form
realInitialWave = np.exp(-1 / 2 * (x - x_0) ** 2 / (sigma_0) ** 2) * np.cos(k_0 * x)
imagInitialWave = np.exp(-1 / 2 * (x - x_0) ** 2 / (sigma_0) ** 2) * np.sin(k_0 * x)

# different potentials
noPotential = np.zeros(N + 1)  # potential is zero everywhere
harmonicPotential = np.linspace(-10, 10, N + 1) ** 2  # harmonic potential (quadratic)
stepPotential = np.zeros(N + 1)
stepPotential[int(N / 2)] = 1  # potential barrier at N/2

# setting the potential
potential = noPotential

# calculating the probability density
probDensity = SL(realInitialWave, imagInitialWave, potential, delta_x, N, delta_t, T)


# ==============================================================================================
# figure with slider


# Create figure
fig = go.Figure()

# Add traces, one for each slider step
for step in range(0, int(np.ceil(T / delta_t) - 1)):
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="#00CED1", width=6),
            name="𝜈 = " + str(step),
            x=x,
            y=probDensity[:, step],
        )
    )

# Make 10th trace visible
fig.data[10].visible = True

# Create and add slider
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[
            {"visible": [False] * len(fig.data)},
            {"title": "Slider switched to time: " + str(i)},
        ],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [
    dict(active=10, currentvalue={"prefix": "Timestep: "}, pad={"t": 50}, steps=steps)
]

fig.update_layout(sliders=sliders)

fig.show()
