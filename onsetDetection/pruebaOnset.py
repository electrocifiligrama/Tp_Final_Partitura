#pruebaOnset

import onsetAlgorithms as onset
from scipy.io import wavfile as wav
import numpy as np
from matplotlib import pyplot as plt

import scipy.signal as signal



AUDIO_PATH = ".\\Audios"


def onsetProcessing(wavName, onsetAlgorithm):
    file_path = AUDIO_PATH + wavName
    f_s, audio = wav.read(file_path)

    result, timeRes= onsetAlgorithm(audio[:, 1], f_s) 
    print(timeRes)
    maxTime = timeRes * (len(result) - 1)
    nT = np.linspace(0, maxTime , len(result))

    audioSize = len(audio[:, 1])
    n = np.linspace(0, (audioSize-1)/f_s, audioSize)

    return result, nT, audio[:, 1], n, timeRes
#variable threshold para descartar falsos positivos

#prueba de los algoritmos HFC (High Frecuency Content) y CDC (Complex Domain Combination)

plotIntermediateOption = False

resultHFC, nHFC, audio1, n1, timeRes = onsetProcessing("\\doMIsolDO.wav", onset.HFC)

#ploteo para evidenciar resultados

fig = plt.figure()
plt.subplot(311)
plt.plot(n1,audio1) #subplot de la señal original


plt.subplot(312)
plt.plot(nHFC,resultHFC) #ploteo de la función de detección

peaks, _ = signal.find_peaks(resultHFC, height = 0, threshold= 10)
NfalsePositives = 0

#cuento la cantidad de falsos positivos
for i in range(0, len(peaks)):
    if resultHFC[peaks[i]] > thresholdOn:
        NfalsePositives += 1
print(NfalsePositives)

#creo vector que NO tenga en cuenta los falsos positivos
peaksAux = np.zeros(len(peaks)-NfalsePositives, dtype=int)

#lleno el nuevo vector con los picos válidos
j = 0
for i in range(0, len(peaks)):
    if resultHFC[(peaks[i])] > thresholdOn:
        peaksAux[j] = peaks[i]
        j += 1  

#genero un vector para guardar los Offsets (finalización de nota), el cual es del mismo tamaño que el vector de peaksAux (Onsets Válidos)

offsets = np.zeros(len(peaksAux), dtype = int)

isOffsetDetected = False #genero flag para saber si se detecta offset o llega una nota antes de que la anterior se termine

for i in range(0, len(peaksAux)): #utilizo todos los onsets para hallar los offsets
    print(i)
    isOffsetDetected = False #reseteo flag

    if i < (len(peaksAux)-1): #si no estoy en el ultimo pico (se toma el ultimo pico como un caso particular)
        current = peaksAux[i]  #marco desde que pico comenzar a buscar
        limit = peaksAux[i+1]  #como mucho busco hasta el proximo pico

    else: #estoy en el ulitmo pico
        current = peaksAux[i]
        limit = len(resultHFC)

    while( (current < limit) and (not isOffsetDetected) ):  #incio la busqueda

        if resultHFC[current] < thresholdOff:  #se logra hallar un offset
            isOffsetDetected = True

        current += 1
        
    #al salir del ciclo while completo el offset
    offsets[i] = current


            


plt.plot(peaksAux*timeRes, resultHFC[peaksAux], 'x')
plt.plot(offsets*timeRes, resultHFC[offsets], 'x')


plt.show()





#SDn, n2 = SD(audio[:,1], f_s)
#Laudio = len(audio[:, 1])

#Ntimes = len(n)
#Ntimes2 = len(n2)

#NperBinTime = Laudio/Ntimes
#print(NperBinTime)
#resTime = Ntimes/n[Ntimes-1]
#print(resTime)




#downsampling e interpolacion


#EnDOWN = signal.decimate(En, 4)
#EnUP = signal.resample(EnDOWN, len(EnDOWN)*4)
#Nup = len(EnUP)
#plt.subplot(414)
#t2 = np.linspace(start=0,stop=n[Ntimes-1],num=Nup)
#plt.plot(t2,EnUP*(-1))


