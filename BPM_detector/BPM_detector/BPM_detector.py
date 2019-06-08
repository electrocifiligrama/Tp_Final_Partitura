from scipy.io import wavfile as wav
from matplotlib import pyplot as plt
import numpy as np
import OSS_generator as o_gen
AUDIO_PATH = ".\\Audios"

file_path = AUDIO_PATH+"\\archer-theme-song.wav"
f_s, audio = wav.read(file_path)
number_of_audios = 1
if ( (audio.shape)[1] > 1):
    number_of_audios = 2
for i in range(0,1):
    if i >0:
        oss_signal += o_gen.GenerateOSS(audio[:,i],f_s)
        oss_signal /= 2
    else:
        oss_signal = o_gen.GenerateOSS(audio[:,i],f_s)
fig = plt.figure()
plt.subplot(211)
t = np.linspace(start=0,stop=(audio.shape[0])/f_s,num=audio.shape[0])
plt.plot(t,audio[:,0])
plt.subplot(212)
t = np.linspace(start=0,stop=len(audio)/f_s,num=len(oss_signal))
plt.plot(t,oss_signal)
plt.show()