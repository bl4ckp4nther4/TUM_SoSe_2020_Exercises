import numpy as np
import random as rand

v_1 = [0, 1]
v_2 = [1, 0]
v_3 = [-1, 0]

vertex = np.zeros((2, 3))
vertex[:, 0] = v_1
vertex[:, 1] = v_2
vertex[:, 2] = v_3

print(vertex)

p = [0.2, 0.2]

points = [p]

for i in range(1, 11):
    j = int(np.ceil(rand.random()*3) - 1)
    print(j)
    p = 1/2 * (p + vertex[:, j])
    points = np.append(points, p)

print()
