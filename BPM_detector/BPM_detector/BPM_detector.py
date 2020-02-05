from scipy.io import wavfile as wav
from matplotlib import pyplot as plt
import numpy as np
import OSS_generator as o_gen
import BPM_FFT as b
from scipy import stats
AUDIO_PATH = ".\\Audios"

file_path = AUDIO_PATH+"\\06-RunToTheHills.wav"
f_s, audio = wav.read(file_path)
number_of_audios = 1
if ( len(audio.shape) > 1):
    number_of_audios = 2
samples = 375
n_fft =2048
alpha = 0.85
bpm1 = [] #Bpm para el primer audio 
bpm2 = [] #Bpm del segundo audio (Solo se utiliza para audios en stereo)
counter = 0
bpm = 0
detector = b.BPM_Detctor( n_fft )

desired_time = 5 #Hasta que segundo de la cancion se quiere sacar el bpm
counter_limit = int( desired_time*f_s )

while counter < counter_limit:
    stop = counter + samples
    if stop >= len(audio):
        stop = -1
    if number_of_audios > 1:
        for i in range(0,number_of_audios):
            buffer =  audio[counter:stop,i] / max( audio[:,i] ) 
            if i >0:
                bpm = detector.BPM_estimate(buffer,f_s,alpha)
                bpm2.append( bpm )
            else:
                bpm = detector.BPM_estimate(buffer,f_s,alpha)
                bpm1.append( bpm )
    else:
        buffer =  audio[counter:stop] / max( audio )
        bpm = detector.BPM_estimate(buffer,f_s,alpha)
        bpm1.append( bpm )
    counter += samples

fig = plt.figure()
if number_of_audios<1:
    t= np.linspace(start=0,stop=(desired_time),num=len(bpm1) )
else:
    t= np.linspace(start=0,stop=(desired_time),num=len(bpm1) )
plt.subplot(211)
plt.plot(t,bpm1)
if number_of_audios > 1:
    plt.subplot(212)
    plt.plot(t,bpm2)
plt.show()
for i in range(0,len(bpm1)):
    bpm1[i] = int(round(bpm1[i]))
    #bpm2[i] = int(round(bpm2[i]))
mode1,a =stats.mode(bpm1,axis=None)
#mode2,a = stats.mode(bpm2,axis=None)
print(mode1[0])
#print(mode2[0])
