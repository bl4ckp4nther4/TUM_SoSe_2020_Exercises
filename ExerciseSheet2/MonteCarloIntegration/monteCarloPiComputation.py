import random

N = 10000000

countInCircle = 0

for i in range(N):
    x = random.random()
    y = random.random()
    if x**2 + y**2 < 1:
        countInCircle = countInCircle + 1

print(4*countInCircle/N)
