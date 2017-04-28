#!/usr/bin/env python

'''Compares correlations of the different wav files'''

from scipy.io import wavfile
import scipy.signal as scp
import numpy as np
import operator
from matplotlib import pyplot as plt


path01 = "../soundfiles/0-1.wav"
path02 = "../soundfiles/0-2.wav"
path03 = "../soundfiles/0-3.wav"
path04 = "../soundfiles/0-4.wav"
path11 = "../soundfiles/1-1.wav"
path12 = "../soundfiles/1-2.wav"
path13 = "../soundfiles/1-3.wav"
path14 = "../soundfiles/1-4.wav"
path22 = "../soundfiles/2-2.wav"
path23 = "../soundfiles/2-3.wav"
path24 = "../soundfiles/2-4.wav"
path33 = "../soundfiles/3-3.wav"
path34 = "../soundfiles/3-4.wav"
pathm11 = "../soundfiles/m1-1.wav"
pathm12 = "../soundfiles/m1-2.wav"
pathm13 = "../soundfiles/m1-3.wav"
pathm14 = "../soundfiles/m1-4.wav"
pathm22 = "../soundfiles/m2-2.wav"
pathm23 = "../soundfiles/m2-3.wav"
pathm24 = "../soundfiles/m2-4.wav"
pathm33 = "../soundfiles/m3-3.wav"
pathm34 = "../soundfiles/m3-4.wav"


rate01, data01 = wavfile.read(path01)
rate02, data02 = wavfile.read(path02)
rate03, data03 = wavfile.read(path03)
rate04, data04 = wavfile.read(path04)
rate11, data11 = wavfile.read(path11)
rate12, data12 = wavfile.read(path12)
rate13, data13 = wavfile.read(path13)
rate14, data14 = wavfile.read(path14)
rate22, data22 = wavfile.read(path22)
rate23, data23 = wavfile.read(path23)
rate24, data24 = wavfile.read(path24)
rate33, data33 = wavfile.read(path33)
rate34, data34 = wavfile.read(path34)
ratem11, datam11 = wavfile.read(pathm11)
ratem12, datam12 = wavfile.read(pathm12)
ratem13, datam13 = wavfile.read(pathm13)
ratem14, datam14 = wavfile.read(pathm14)
ratem22, datam22 = wavfile.read(pathm22)
ratem23, datam23 = wavfile.read(pathm23)
ratem24, datam24 = wavfile.read(pathm24)
ratem33, datam33 = wavfile.read(pathm33)
ratem34, datam34 = wavfile.read(pathm34)

soundTagList = ["data01", "data02", "data03", "data04", "data11", "data12", "data13", 
"data14", "data22", "data23", "data24", "data33", "data34", "datam11", "datam12", 
"datam13", "datam14", "datam22", "datam23", "datam24", "datam33", "datam34"]

soundList = [data01, data02, data03, data04, data11, data12, data13, data14, data22, data23, 
data24, data33, data34, datam11, datam12, datam13, datam14, datam22, datam23, datam24, 
datam33, datam34]

corrList = []

# for d in soundList:
# 	# left is the data from channel 0.
# 	left = d[45000:50000, 0].astype(np.float64)

# 	# right is the data from channel 1.
# 	right = d[45000:50000, 1].astype(np.float64)

# 	corr = scp.correlate(left, right)

# 	index, res = max(enumerate(corr),  key=operator.itemgetter(1))
# 	corrList.append(index)

# 	if d is datam13:
# 		y = corr
# 		plt.plot(y)
# 		plt.show()

# corrTups = zip(soundTagList, corrList)

#print corrTups

sampleLen = 2000;
maxList = []

for j in soundList:
	for i in range(2000, len(j)+1, sampleLen):
		left = j[i-sampleLen:i, 0].astype(np.float64)
		right = j[i-sampleLen:i, 1].astype(np.float64)
		corr = scp.correlate(left, right, mode='same', method='direct')
		index, res = max(enumerate(corr),  key=operator.itemgetter(1))
		corrList.append(index)
	maxList.append(max(corrList))
maxTups = zip(soundTagList, maxList)
print maxTups

# plt.hist(corrList)
# plt.xlabel("Samples")
# plt.ylabel("Correlation")
# plt.show()s