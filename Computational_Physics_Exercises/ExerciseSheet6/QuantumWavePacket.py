import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def SL(realInitialWave, imagInitialWave, potential, delta_x, N, delta_t, T):
    realWaveFkt = np.zeros([N+1, int(T/delta_t + 1)])
    imagWaveFkt = np.zeros([N+1, int(T/delta_t + 1)])

    realWaveFkt[:, 0] = realInitialWave
    imagWaveFkt[:, 0] = imagInitialWave

    for n in range(0, int(np.ceil(T/delta_t)-1)):
        t = n*delta_t
        print(n)
        realWaveFkt[:,n+1] = realWaveFkt[:,n] + 2*(delta_t/delta_x**2 + potential*delta_t)*imagWaveFkt[:,n] - delta_t/delta_x**2 * (shiftPlus(imagWaveFkt[:,n]) + shiftMinus(imagWaveFkt[:,n]))
        imagWaveFkt[:,n+1] = imagWaveFkt[:,n] - 2*(delta_t/delta_x**2 + potential*delta_t)*realWaveFkt[:,n+1] - delta_t/delta_x**2 * (shiftPlus(realWaveFkt[:,n+1]) + shiftMinus(realWaveFkt[:,n+1]))

    probDensity = realWaveFkt**2 + imagWaveFkt**2
    return probDensity


def shiftPlus(array):
    # shifting all elements of the array up
    N = len(array)
    newArray = np.zeros(N)
    for i in range(0, N-1):
        if i == N:
            newArray[N-1] = array[0]
        else:
            newArray[i] = array[i+1]
    return newArray

def shiftMinus(array):
    # shifting all elements of the array down
    N = len(array)
    newArray = np.zeros(N)
    for i in range(0, N-1):
        if i == 0:
            newArray[0] = array[N-1]
        else:
            newArray[i] = array[i-1]
    return newArray

sigma_0 = 0.5
k_0 = 17 * np.pi # k_0 = 0
delta_x = 0.01
x_0 = 5

start = 0
end = 10
N = 100
delta_x = (end - start)/N
x = np.linspace(start, end ,N+1)

delta_t = (delta_x/2)**2
T = 0.1

realInitialWave = np.exp(-1/2 *  (x - x_0)**2/(sigma_0)**2)*np.cos(k_0 * x)
imagInitialWave = np.exp(-1/2 *  (x - x_0)**2/(sigma_0)**2)*np.sin(k_0 * x)


noPotential = np.zeros(N+1)
infiniteWalls = np.zeros(N+1)
infiniteWalls[0] = 1e50
infiniteWalls[N] = 1e50
harmonicPotential = np.linspace(-10,10,N+1)**2
stepPotential = np.zeros(N+1)
stepPotential[int(N/2):N+1] = 1

potential = noPotential

waveFunction = SL(realInitialWave, imagInitialWave, potential, delta_x, N, delta_t, T)
probDensity = abs(waveFunction)**2


#==============================================================================================
#figure with slider


# Create figure
fig = go.Figure()

# Add traces, one for each slider step
for step in range(0, int(np.ceil(T/delta_t)-1)):
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="#00CED1", width=6),
            name="𝜈 = " + str(step),
            x=x,
            y=probDensity[:,step]
        )
    )

# Make 10th trace visible
fig.data[10].visible = True

# Create and add slider
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Slider switched to step: " + str(i)}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=10,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)

fig.show()