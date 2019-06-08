from scipy.io import wavfile as wav
from matplotlib import pyplot as plt
import numpy as np
import OSS_generator as o_gen
import BPM_FFT as b
AUDIO_PATH = ".\\Audios"

file_path = AUDIO_PATH+"\\146_BPM_bumblebee.wav"
f_s, audio = wav.read(file_path)
number_of_audios = 1
if ( len(audio.shape) > 1):
    number_of_audios = 2
chunk_size = 10*44100
bpm1 = [] #Bpm para el primer audio 
bpm2 = [] #Bpm del segundo audio (Solo se utiliza para audios en stereo)
counter = 0
while counter < len(audio):
    stop = counter + chunk_size
    if stop >= len(audio):
        stop = -1
    if number_of_audios > 1:
        for i in range(0,number_of_audios):
            buffer = audio[counter:stop,i]
            if i >0:
                bpm2.append( b.BPM_estimate(buffer,f_s,n_samples=512) )
            else:
                bpm1.append( b.BPM_estimate(buffer,f_s,n_samples=512) )
    else:
        buffer = audio[counter:stop]
        bpm1.append( b.BPM_estimate(buffer,f_s,n_samples=512) )
    counter += chunk_size

fig = plt.figure()
plt.subplot(211)
plt.plot(bpm1)
if number_of_audios > 1:
    plt.subplot(212)
    plt.plot(bpm2)
plt.show()

