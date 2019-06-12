#pruebaOnset

import onsetAlgorithms as onset
from scipy.io import wavfile as wav
import numpy as np
from matplotlib import pyplot as plt

AUDIO_PATH = ".\\Audios"

#prueba de los algoritmos HFC (High Frecuency Content) y CDC (Complex Domain Combination)

plotIntermediateOption = False

resultHFC, nHFC = onsetProcessing("\\doMIsolDO.wav", onset.HFC, plotIntermediateOption)

resultCDC, nCDC = onsetProcessing("\\doMIsolDO.wav", onset.CDC, plotIntermediateOption)




def onsetProcessing(wavName, onsetAlgorithm):
file_path = AUDIO_PATH + wavName
f_s, audio = wav.read(file_path)

result, timeRes= onsetAlgorithm(audio[:, 1], f_s) 

maxTime = timeRes * (len(result) - 1)
nT = np.linspace(0, maxTime , len(result))

return result, nT




SDn, n2 = SD(audio[:,1], f_s)
Laudio = len(audio[:, 1])

Ntimes = len(n)
Ntimes2 = len(n2)

NperBinTime = Laudio/Ntimes
print(NperBinTime)
resTime = Ntimes/n[Ntimes-1]
print(resTime)
fig = plt.figure()
plt.subplot(411)

t1 = np.linspace(start=0,stop=(audio.shape[0])/f_s,num=audio.shape[0])
plt.plot(t1,audio[:,0])
plt.subplot(412)
t2 = np.linspace(start=0,stop=n[Ntimes-1],num=Ntimes)
plt.plot(t2,En)
plt.subplot(413)
t3 = np.linspace(start=0,stop=n2[Ntimes-1],num=Ntimes2)
plt.plot(t3,SDn)



#downsampling e interpolacion


EnDOWN = signal.decimate(En, 4)
EnUP = signal.resample(EnDOWN, len(EnDOWN)*4)
Nup = len(EnUP)
plt.subplot(414)
t2 = np.linspace(start=0,stop=n[Ntimes-1],num=Nup)
plt.plot(t2,EnUP*(-1))


plt.show()