from scipy.io import wavfile
import numpy as np
import os

def continuously_read():
    while True:
        os.system("ssh pi@192.168.17.201 /home/pi/use_case_scripts/Audio_Loc_copy.sh > temp.wav")
        os.system("aplay ./temp.wav")

        rate, data = wavfile.read("./temp.wav")
        # left is the data from channel 0.
        left = data[:, 0]
        # right is the data from channel 1.
        right = data[:, 1]
        print left

def sound_correlation(start, sample_len, left, right):
    left = left.astype(np.float32)
    right = right.astype(np.float32)
    sample = left[start:start + sample_len]
    correlation = np.correlate(sample, right[start:])
    print correlation
    return np.argmax(correlation)

def test_correlation():
    path = "/home/sean/catkin_ws/src/ride-of-the-neatos/soundfiles/0-2.wav"
    rate, data = wavfile.read(path)
    print type(data)
    # left is the data from channel 0.
    left = data[:, 0]
    # right is the data from channel 1.
    right = data[:, 1]

    print sound_correlation(0, 2100, left, right)
