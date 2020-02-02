from scipy.io import wavfile as wav
from matplotlib import pyplot as plt
import numpy as np
import OSS_generator as o_gen
import BPM_FFT as b
from scipy import stats
AUDIO_PATH = ".\\Audios"

file_path = AUDIO_PATH + "\\87_BPM_Monk.wav"
f_s, audio = wav.read(file_path)
number_of_audios = 1
if len(audio.shape) > 1:
    number_of_audios = 2
samples = 375
chunk_size = 2048*samples
alpha = 0.85
bpm1 = []   # Bpm para el primer audio
bpm2 = []   # Bpm del segundo audio (Solo se utiliza para audios en stereo)
counter = 0
bpm = 0
power1 = 0
power2 = 0
while counter < len(audio):
    stop = counter + chunk_size
    if stop >= len(audio):
        stop = -1
    if number_of_audios > 1:
        for i in range(0, number_of_audios):
            buffer = audio[counter:stop, i]
            if i > 0:
                bpm, power2 = b.BPM_estimate(buffer, f_s, samples, alpha, power2)
                bpm2.append(bpm)
            else:
                bpm, power1 = b.BPM_estimate(buffer, f_s, samples, alpha, power1)
                bpm1.append(bpm)
    else:
        buffer = audio[counter:stop]
        bpm, power1 = b.BPM_estimate(buffer, f_s, samples, alpha, power1)
        bpm1.append(bpm)
    counter += chunk_size

fig = plt.figure()
if number_of_audios < 1:
    t = np.linspace(start=0, stop=(len(audio)/f_s), num=len(bpm1))
else:
    t = np.linspace(start=0, stop=(audio.shape[0]/f_s), num=len(bpm1))
plt.subplot(211)
plt.plot(t, bpm1)
if number_of_audios > 1:
    plt.subplot(212)
    plt.plot(t, bpm2)
plt.show()
for i in range(0, len(bpm1)):
    bpm1[i] = int(round(bpm1[i]))
    # bpm2[i] = int(round(bpm2[i]))
mode1, a = stats.mode(bpm1, axis=None)
# mode2,a = stats.mode(bpm2,axis=None)
print(mode1[0])
# print(mode2[0])
