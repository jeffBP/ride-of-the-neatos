from scipy.io import wavfile
import scipy.signal as scp
import numpy as np
import operator
from matplotlib import pyplot as plt


path = "../soundfiles/out6.wav"

print "here1"

rate, data = wavfile.read(path)
# left is the data from channel 0.
print "here2"
left = data[44000:45000, 0].astype(np.float64)
# right is the data from channel 1.
print "here3"
print left[1:10]
right = data[44000:45000, 1].astype(np.float64)
print right[1:10].dtype

print "here4"
print len(right)
corr = scp.correlate(right, left)
print "here5", corr
index, res = max(enumerate(corr),  key=operator.itemgetter(1))

print index, res
print corr[997]

x = np.arange(0, 100, 1000);
y = corr
plt.plot(y)
plt.show()