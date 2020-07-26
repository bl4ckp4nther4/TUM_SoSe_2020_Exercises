import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def calculateStaggeredTimesteps(Parameters, InitialWave, potential):
    # calculating the probability density of of all timesteps and points in space
    sectionCount = Parameters.sectionCount
    sectionSize = Parameters.sectionSize
    totalTime = Parameters.totalTime
    timestepSize = Parameters.timestepSize

    # initializing the 2D arrays for real part imag part and prob density
    realWF = np.zeros([sectionCount + 1, int(totalTime / timestepSize + 1)])
    imagWF = np.zeros([sectionCount + 1, int(totalTime / timestepSize + 1)])
    probDensity = np.zeros([sectionCount + 1, int(totalTime / timestepSize + 1)])

    # we need the first two initial wavepackets
    realWF[:, 0] = realWF[:, 1] = InitialWave.real
    imagWF[:, 0] = imagWF[:, 1] = InitialWave.imag

    # going through all time steps
    for timeIndex in range(0, int(np.ceil(totalTime / timestepSize) - 1)):

        # setting the borders to 0
        realWF[0, timeIndex + 1] = 0
        realWF[sectionCount, timeIndex + 1] = 0
        imagWF[0, timeIndex + 1] = 0
        imagWF[sectionCount, timeIndex + 1] = 0

        # going through all positions for the real part
        for spaceIndex in range(1, sectionCount - 1):

            # setting the real part of the wavefunction according to the lecture
            realWF[spaceIndex, timeIndex + 1] = realWF[
                spaceIndex, timeIndex - 1
            ] + 2 * timestepSize * (
                potential[spaceIndex] * imagWF[spaceIndex, timeIndex]
                + 1
                / sectionSize ** 2
                * (
                    imagWF[spaceIndex - 1, timeIndex]
                    + imagWF[spaceIndex + 1, timeIndex]
                    - 2 * imagWF[spaceIndex, timeIndex]
                )
            )
        # going trough all the positions for the imag part
        for spaceIndex in range(1, sectionCount - 1):

            # setting the imaginary part of the wavefunction according to the lecture
            imagWF[spaceIndex, timeIndex + 1] = imagWF[
                spaceIndex, timeIndex - 1
            ] - 2 * timestepSize * (
                potential[spaceIndex] * realWF[spaceIndex, timeIndex]
                + 1
                / sectionSize ** 2
                * (
                    realWF[spaceIndex - 1, timeIndex]
                    + realWF[spaceIndex + 1, timeIndex]
                    - 2 * realWF[spaceIndex, timeIndex]
                )
            )
        # setting the probability density after calculating each time step
        probDensity[:, timeIndex + 1] = (
            realWF[:, timeIndex] ** 2 + imagWF[:, timeIndex] ** 2
        )

    return probDensity


class Parameters:
    leftBorder = 0  # left border of space
    rightBorder = 10  # right border of space
    sectionCount = 100  # number of sections in space (number of points = N+1)
    sectionSize = (
        rightBorder - leftBorder
    ) / sectionCount  # size of one section in space

    timestepSize = (sectionSize / 2) ** 2  # timesteps
    totalTime = timestepSize * 1000  # total time


class InitialWave(Parameters):
    space = np.linspace(
        Parameters.leftBorder, Parameters.rightBorder, Parameters.sectionCount + 1
    )
    wavePacketStart = (
        3 / 4 * (Parameters.rightBorder - Parameters.leftBorder)
    )  # starting point of the wavepacket
    wavePacketWidth = (
        Parameters.rightBorder - Parameters.leftBorder
    ) / 10  # width of wavepacket in space
    waveNumber = 17 * np.pi  # k_0 = 0

    # initial wavepacket in real and imaginary form
    real = np.exp(
        -1 / 2 * (space - wavePacketStart) ** 2 / (wavePacketWidth) ** 2
    ) * np.cos(waveNumber * space)
    imag = np.exp(
        -1 / 2 * (space - wavePacketStart) ** 2 / (wavePacketWidth) ** 2
    ) * np.sin(waveNumber * space)


class Potential(Parameters):
    # different potentials
    zero = np.zeros(Parameters.sectionCount + 1)  # potential is zero everywhere
    harmonic = (
        np.linspace(-10, 10, Parameters.sectionCount + 1) ** 2
    )  # harmonic potential (quadratic)
    step = np.zeros(Parameters.sectionCount + 1)
    step[int(Parameters.sectionCount / 2)] = 1  # potential barrier at N/2


# calculating the probability density
probDensity = calculateStaggeredTimesteps(Parameters, InitialWave, Potential.zero)


# ==============================================================================================
# figure with slider


# Create figure
fig = go.Figure()

# Add traces, one for each slider step
for timeStep in range(
    0, int(np.ceil(Parameters.totalTime / Parameters.timestepSize) - 1)
):
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="#00CED1", width=6),
            name="𝜈 = " + str(timeStep),
            x=InitialWave.space,
            y=probDensity[:, timeStep],
        )
    )

# Make 10th trace visible
fig.data[10].visible = True

# Create and add slider
steps = []
for index in range(len(fig.data)):
    timeStep = dict(
        method="update",
        args=[
            {"visible": [False] * len(fig.data)},
            {"title": "Slider switched to time: " + str(index)},
        ],  # layout attribute
    )
    timeStep["args"][0]["visible"][index] = True  # Toggle i'th trace to "visible"
    steps.append(timeStep)

sliders = [
    dict(active=10, currentvalue={"prefix": "Timestep: "}, pad={"t": 50}, steps=steps)
]

fig.update_layout(sliders=sliders)

fig.show()
