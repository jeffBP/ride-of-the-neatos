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

    left = d[:, 0].astype(np.float64)
    right = d[:, 1].astype(np.float64)
    corr = scp.correlate(left, right, mode="full", method="auto")
    index, res = max(enumerate(corr),  key=operator.itemgetter(1))
    corrList.append(len(corr)/2 - index)
    samp = max(set(corrList), key=corrList.count)
    print samp
    return samp


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
    return math.degrees(theta)

if __name__ == "__main__":
    samps = getSamples("wavFile.wav")
    ang = sampleToAngle(samps)
    sys.exit(str(ang))
