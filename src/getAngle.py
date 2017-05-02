#!/usr/bin/env python

'''Compares correlations of the different wav files'''
import math
from scipy.io import wavfile
import scipy.signal as scp
import numpy as np
import operator
from matplotlib import pyplot as plt
import sys


def getSamples(file_name):
    sampleLen = 2000;
    modeList = []
    r, d = wavfile.read(file_name)
    corrList = []
    for i in range(4000, len(d)+1, 2000):
        left = j[i-4000:i, 0].astype(np.float64)
        right = j[i-3000: i-1000, 1].astype(np.float64)
        corr = scp.correlate(left, right, mode="valid", method="auto")
        index, res = max(enumerate(corr),  key=operator.itemgetter(1))
        corrList.append(len(corr)/2 - index)
    modeList.append(max(set(corrList), key=corrList.count))
    plt.hist(corrList)
    plt.xlabel("Samples")
    plt.ylabel("Correlation")
    plt.show()
    maxTups = zip(["d2_40", "d2_01", "d2_m16"], modeList)
    return maxTups


def sampleToAngle(n):
    """
    Function that takes the sample difference between 2 mics
    and returns the angle away that the sound source is.
    Arguments: Number of Samples (n)
    Returns: Angle of source (theta)
    """
    if n > 42.695:
        x = 42.695
    elif n < -42.695:
        x = -42.695
    else:
        x = n
    A = 340.29/(44100*0.0254)
    denom = math.sqrt(20905*A**2*x**2 - A**4 * x**4)
    numer = 1872
    theta = math.acos(denom/numer)
    if n  < 0:
        theta = -theta
    return theta

if __name__ == "__main__":
    samps = getSamples("wavFile.wav")
    ang = sampleToAngle(samps)
    sys.exit(str(ang))
