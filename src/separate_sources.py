from scipy.io import wavfile
import scipy.signal as scp
import numpy as np

path = "../soundfiles/out6.wav"

print "here1"

rate, data = wavfile.read(path)
# left is the data from channel 0.
print "here2"
left = data[44000:45000, 0]
# right is the data from channel 1.
print "here3"
print left[1:10]
right = data[44000:45000, 1]
print right[1:10]

print "here4"
print len(right)
corr = scp.correlate(right, left)
print "here5"
res = max(corr)

print res