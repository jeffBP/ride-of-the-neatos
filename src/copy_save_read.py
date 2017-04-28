from scipy.io import wavfile
import os

while True:
    os.system("ssh pi@192.168.17.201 /home/pi/use_case_scripts/Record_from_lineIn_Micbias.sh | arecord -f S32_LE --rate=44100 -c2 -q -d 1 temp.wav")

    rate, data = wavfile.read("./temp.wav")
    # left is the data from channel 0.
    left = data[:, 0]
    # right is the data from channel 1.
    right = data[:, 1]

    print left
