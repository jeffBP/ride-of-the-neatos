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
    """
    Takes a file name, extracts stereo sound,
    and then performs cross correlation to
    determine the offse, in samples.
    Arguments: file_name
    Returns: samps, the offset measured in samples
    """
    sampleLen = 2000;
    modeList = []
    r, d = wavfile.read(file_name)
    corrList = []

    #Identify the two separate channels
    left = d[:, 0].astype(np.float64)
    right = d[:, 1].astype(np.float64)

    #Perform correlation on entire sound sample
    corr = scp.correlate(left, right, mode="full", method="auto")
    index, res = max(enumerate(corr),  key=operator.itemgetter(1))
    corrList.append(len(corr)/2 - index)
    samp = max(set(corrList), key=corrList.count)
    return samp


def sampleToAngle(n):
    """
    Function that takes the sample difference between 2 mics
    and returns the angle away that the sound source is.
    Arguments: Number of Samples (n)
    Returns: Angle of source (theta)
    """

    #If it's larger than this, the microhpnes shifted a bit
    if n > 42.695:
        x = 42.695
    elif n < -42.695:
        x = -42.695
    else:
        x = n

    #Identify whether sound is to the left or right
    #Compute angle based on that
    A = 340.29/(44100*0.0254)
    if n > 0:
        denom = math.sqrt(20905*A**2*x**2 - A**4 * x**4)
    else:
        denom = -math.sqrt(20905*A**2*x**2 - A**4 * x**4)

    #Numer is based on number of samples expected
    numer = 1872
    theta = math.acos(denom/numer)

    return (90 - math.degrees(theta))

if __name__ == "__main__":
    samps = getSamples("wavFile.wav")
    ang = sampleToAngle(samps)
    sys.exit(str(ang))
