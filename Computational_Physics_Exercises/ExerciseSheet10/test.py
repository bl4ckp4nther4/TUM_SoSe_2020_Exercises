import time
import sys
import numpy as np


def setBar():
    toolbar_width = 100

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['


def updateBar(progress, lastUpdate):
    delta = int(np.floor(progress) - lastUpdate)
    for i in range(0, delta):
        sys.stdout.write("-")
        sys.stdout.flush()
    return np.floor(progress)


N = 1000
setBar()
lastUpdate = 0
for i in range(N):
    time.sleep(0.01)  # do real work here
    # update the bar
    lastUpdate = updateBar(100 * i / N, lastUpdate)

