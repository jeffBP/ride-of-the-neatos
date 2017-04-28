#!/usr/bin/env python
from scipy.io import wavfile
import scipy.signal as scp
import numpy as np
import math
import operator
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def getAvg(path):
    rate, data = wavfile.read(path)
    # left is the data from channel 0.

    left = data[:, 0].astype(np.float64)
    # right is the data from channel 1.

    right = data[:, 1].astype(np.float64)

    posCounter = 0
    negCounter = 0
    sumleftPos = 0
    sumleftNeg = 0
    sumrightPos = 0
    sumrightNeg = 0

    for i in left:
        if i > 0:
            sumleftPos += i
            posCounter += 1
        else:
            sumleftNeg += i
            negCounter += 1
    leftPosAvg = sumleftPos/posCounter
    leftNegAvg = sumleftNeg/negCounter

    posCounter = 0
    negCounter = 0
    for i in right:
        if i > 0:
            sumrightPos += i
            posCounter += 1
        else:
            sumrightNeg += i
            negCounter += 1


    rightPosAvg = sumrightPos/posCounter
    rightNegAvg = sumrightNeg/negCounter

    return (leftPosAvg, leftNegAvg, rightPosAvg, rightNegAvg)
coords =   [(-1, 1),
             (0, 1),
             (1, 1),
             (-2, 2),
             (-1, 2),
             (0, 2),
             (1, 2),
             (2, 2),
             (-3, 3),
             (-2, 3),
             (-1, 3),
             (0, 3),
             (1, 3),
             (2, 3),
             (3, 3),
             (-3, 4),
             (-2, 4),
             (-1, 4),
             (0, 4),
             (1, 4),
             (2, 4),
             (3, 4)]

coordsStraight = [(1, 1), (2, 2), (3, 3)]
pathsStraight = ['../soundfiles/1-1.wav', '../soundfiles/2-2.wav', '../soundfiles/3-3.wav']
paths = ['../soundfiles/m1-1.wav',
         '../soundfiles/0-1.wav',
         '../soundfiles/1-1.wav',
         '../soundfiles/m2-2.wav',
         '../soundfiles/m1-2.wav',
         '../soundfiles/0-2.wav',
         '../soundfiles/1-2.wav',

         '../soundfiles/2-2.wav',
         '../soundfiles/m3-3.wav',
         '../soundfiles/m2-3.wav',
         '../soundfiles/m1-3.wav',
         '../soundfiles/0-3.wav',
         '../soundfiles/1-3.wav',
         '../soundfiles/2-3.wav',
         '../soundfiles/3-3.wav',
         '../soundfiles/m3-4.wav',
         '../soundfiles/m2-4.wav',
         '../soundfiles/m1-4.wav',
         '../soundfiles/0-4.wav',
         '../soundfiles/1-4.wav',
         '../soundfiles/2-4.wav',
         '../soundfiles/3-4.wav'
         ]

leftPosAvgs = []
leftNegAvgs = []
rightPosAvgs = []
rightNegAvgs = []
distances = []

for i in paths:
    leftPos, leftNeg, rightPos, rightNeg = getAvg(i)
    leftPosAvgs.append(leftPos/1000)
    leftNegAvgs.append(leftNeg/1000)
    rightPosAvgs.append(rightPos/1000)
    rightNegAvgs.append(rightNeg/1000)

for i in coordsStraight:
    distances.append(math.sqrt(i[0]**2 + i[1]**2))
x = [int(i[0]) for i in coords]
y = [int(i[1]) for i in coords]

fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(x, y, leftPosAvgs)
plt.xlabel('Distance(ft)')
plt.ylabel('Distance(ft)')
plt.title('Amplitude Surface')
plt.show()
# plt.figure(1)
# plt.plot(distances, leftPosAvgs, 'bo')
# plt.title('Left Channel Positive Averages')
# plt.xlabel('Distance (ft)')
# plt.ylabel('Amplitude x10^3')
# plt.figure(2)
# plt.plot(distances, leftNegAvgs, 'bo')
# plt.title('Left Channel Negative Averages')
# plt.xlabel('Distance (ft)')
# plt.ylabel('Amplitude x10^3')
# plt.figure(3)
# plt.plot(distances, rightPosAvgs, 'ro')
# plt.title('Right Channel Positive Averages')
# plt.xlabel('Distance (ft)')
# plt.ylabel('Amplitude x10^3')
# plt.figure(4)
# plt.plot(distances, rightNegAvgs, 'ro')
# plt.title('Right Channel Negative Averages')
# plt.xlabel('Distance (ft)')
# plt.ylabel('Amplitude x10^3')
# plt.show()
