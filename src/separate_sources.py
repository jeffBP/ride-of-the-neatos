from scipy.io import wavfile

path = "./out.wav"

rate, data = wavfile.read(path)
# left is the data from channel 0.
left = data[:, 0]
# right is the data from channel 1.
right = data[:, 1]

print left