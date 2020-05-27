import math
import random
import numpy as np
from matplotlib import image as im
from matplotlib import pyplot as plt
from scipy import stats


class fractalImage:
    fractalRGB = np.zeros((32, 32))
    fractalOneColor = np.zeros((32, 32))
    fractalBin = np.zeros((32, 32))
    fractalExtended = np.zeros((32, 32))
    invertedImage = True

    originalSize = (32, 32)
    extendedSize = (32, 32)

    # number of deviding iterations
    iterations = 5

    # ratio of filled boxes
    totalNoBoxes = np.zeros(iterations)
    fillRatio = np.zeros(iterations)

    slope = 0
    intercept = 0

    def __init__(self, imPath, invertedImage):
        self.imPath = imPath
        self.invertedImage = invertedImage

        self.readAndSetImage()
        self.boxCountingAlgorithm()
        self.plotAndFitting()
        self.setFractalDimension()

    def readAndSetImage(self):
        # read the image from disk
        self.fractalRGB = im.imread(self.imPath)
        # take only one color channel from bw image
        self.fractalOneColor = self.fractalRGB[:, :, 0]

        # make the image binary, with the coast being ones
        # image needs to be inverted?
        if self.invertedImage == True:
            self.fractalBin = np.array([self.fractalOneColor < 0.3])[0, :, :]
        else:
            self.fractalBin = np.array([self.fractalOneColor > 0.3])[0, :, :]

        # find frame size around the image with dimensions of power of 2
        self.originalSize = self.fractalBin.shape
        self.extendedSize = (self.roundUpPower2(self.originalSize[0]),
                             self.roundUpPower2(self.originalSize[1]))
        # create frome
        self.fractalExtended = np.zeros(self.extendedSize)
        # insert binary image into extended frame
        self.fractalExtended[0:self.originalSize[0],
                             0:self.originalSize[1]] = self.fractalBin

    def roundUpPower2(self, n):
        n -= 1
        n |= n >> 1
        n |= n >> 2
        n |= n >> 4
        n |= n >> 8
        n |= n >> 16
        n += 1
        return n

    def boxCountingAlgorithm(self):
        self.iterations = int(min(
            (np.log2(self.extendedSize[0]), np.log2(self.extendedSize[1]))))

        # ratio of filled boxes
        self.totalNoBoxes = np.zeros(self.iterations)
        self.fillRatio = np.zeros(self.iterations)

        # devide image in more and more smaller rectangles
        for i in range(0, self.iterations):
            # deviding the image into boxes of this size
            boxShape = np.floor(np.asarray(self.extendedSize) / 2**i)

            # array of boxes filled or not
            boxFilled = np.zeros((2**i, 2**i))

            for x in range(0, 2**i):
                for y in range(0, 2**i):
                    # define endpoints for the box that will be cut out
                    x_start = int(x*boxShape[0])
                    x_end = int((x + 1) * boxShape[0])
                    y_start = int(y*boxShape[1])
                    y_end = int((y + 1) * boxShape[1])

                    # cut out the box
                    cutBox = self.fractalExtended[x_start:x_end, y_start:y_end]

                    # decide if cutBox is filled
                    if (sum(sum(cutBox))) > 0:
                        boxFilled[x, y] = True

            # calculate fraction of filled boxes
            N_total = 2**i * 2**i
            N_filled = sum(sum(boxFilled))

            self.totalNoBoxes[i] = N_total
            self.fillRatio[i] = N_filled/N_total

    def plotAndFitting(self):
        # log-log plot plot
        xData = np.log2(self.totalNoBoxes)
        yData = np.log2(self.fillRatio)
        plt.plot(xData, yData, 'o')

        # linear regression curve fitting
        self.slope, self.intercept, self.r_value, self.p_value, self.std_err = stats.linregress(
            xData, yData)

        # plot the fitted function
        plt.plot(xData,
                 self.intercept + self.slope*xData, 'r')

        plt.show()
        print("slope: ", self.slope)

    def setFractalDimension(self):
        # calculating fractal dimension from slope
        self.fractalDimension = 2 + self.slope
        print("The Fractal Dimension is: ",
              self.fractalDimension)


coastOfNorway = fractalImage(
    'D:/04_Code/02_Computational_Physics/Computational_Physics_2/Computational-Physics-Exercises/Computational_Physics_Exercises/ExerciseSheet5/coastlineNorway.jpg', True)
