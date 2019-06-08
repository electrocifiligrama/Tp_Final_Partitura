import matplotlib.pyplot as plt
import numpy as np
import peakutils
from scipy.signal import fftconvolve , find_peaks , decimate
from scipy.fftpack import rfft , irfft
from collections import deque

# MEJORAS:
# mejorar algoritmo optimize note
# ver de implementar alguno en un Wav

def sgn(data):
    # determino threshold
    max = np.amax(data)
    Cl = 0.68*max
    # aplico transformacion
    data = np.array(data)
    for i in range(0,len(data)):
        if data[i] >= Cl:
            data[i] = 1
        elif data[i] <= -Cl:
            data[i] = -1
        else:
            data[i] = 0
    return data

def optimizeNote(noteData,frames):
    max = np.amax(noteData)
    noteData = deque(noteData)
    while noteData[0] < 0.1*max:
        noteData.popleft()
    noteData = np.array(noteData)
    argMax = np.argmax(noteData)
    length = len(noteData)
    i = 0
    f = length
    if  not (argMax - round(frames/2) <= 0):
        i = argMax - round(frames/2)
    if not (argMax + frames - (argMax - i) >= length):
        f = argMax + frames - (argMax - i)
    noteData = noteData[i:f]
    return noteData

# Si no encuentra frecuencia fundamental, devuelve fo = 44100
# Cuanto mas grande noteData mejor la aproximacion a la fpitch (aprox 3000 minimo)
def autocorrelationAlgorithm(noteData,fs,frames = 3000, clippingStage = "False"):
    fo = 0
    # selecciono mejor parte de la nota
    #plt.figure(1)
    #plt.plot(noteData)
    noteData = optimizeNote(noteData,frames)
    #plt.figure(2)
    #plt.plot(noteData)
    #plt.show()
    # autocorrelacion
    if clippingStage:
        x1 = sgn(noteData)
        x2 = sgn(noteData[::-1])
    else:
        x1 = noteData
        x2 = noteData[::-1]
    correlation = fftconvolve(x1, x2, mode='full')
    correlation = correlation[correlation.size//2:]
    # busco primer maximo
    max = 0.3*np.amax(correlation)
    peaks = find_peaks(correlation,max, distance = 21)
#    for i in range(0,len(peaks[0])):
#        plt.plot(peaks[0][i], correlation[peaks[0][i]], 'ro')
#    plt.plot(correlation)
#    plt.show()
    if len(peaks[0]) > 0:
        xMax = peaks[0][0]
    else:
        xMax = 1
    # determino frequencia
    fo=fs/xMax
    return fo

def harmonicProductSpectrum(noteData,fs,frames = 20000,hNro = 7):
    fo = 0
    noteData = optimizeNote(noteData,frames)
    # aplico ventana
    window = np.hanning(len(noteData))
    noteData = np.multiply(window,noteData)
    # fft de los datos
    fftData = rfft(noteData)
    fftData = abs(fftData[:])
    k = np.arange(len(noteData))
    T = (2*len(noteData))/fs
    fftF = k/T 
    fftArray = []
    fftArray.append(fftData)
    # downsample for un factor de 2 a hNro
    for i in range(2,hNro+1):
        auxfft = decimate(fftData, i)
        auxfft = abs(auxfft[:])
        # relleno con ceros para que coincidan en tamaño 
        cant = len(fftData) - len(auxfft)
        zeros = np.zeros(cant)
        auxfft = np.concatenate((auxfft, zeros))
        fftArray.append(auxfft)
    # multiplico todas las fft de fftArray
    hpsArray = []
    for i in range(0,len(fftData)):
        auxElement = 1
        for j in range(0,hNro):
            auxElement = auxElement*fftArray[j][i]
        hpsArray.append(auxElement)
    # elimino picos antes de los 20Hz
    index = 0
    while fftF[index] < 20:
        index = index+1
    for i in range(0,index):
        hpsArray[i] = 0
    # busco frecuencia del maximo de la nueva funcion
    #plt.plot(hpsArray)
    #plt.show()
    fo = fftF[np.argmax(hpsArray)]
    return fo

def cepstrum(noteData,fs,frames = 3000):
    noteData = optimizeNote(noteData,frames)
    # aplico ventana
    window = np.hanning(len(noteData))
    noteData = np.multiply(window,noteData)
    # calculo cepstrum
    powerSpectrum = np.abs(rfft(noteData))**2
    cepstrum = np.abs(irfft(np.log(powerSpectrum)))**2
    plt.plot(cepstrum)
    plt.show()
    return

def differenceFunction(data,tauMax,fs): # ver de implementar forma con fft
    diff = np.array([], dtype=np.float64)
    t = int(fs*tauMax)
    for i in range(1,t):
        sum = np.float64(0)
        for j in range(0,len(data)-t):
            aux = (data[j]-data[j+i])**2
            sum += aux
        diff = np.append(diff,sum)
    return diff

def CMDF(diff): # cumulative mean normalized difference function
    cmdf = []
    cmdf.append(1)
    for i in range(1,len(diff)):
        sum = 0
        for j in range(1,i):
            sum += diff[j]
        aux=(i*diff[i])/sum
        cmdf.append(aux)
    return cmdf

def selectFoSample(cmdf,th = 0.13):
    sample = 0
    invCmdf = np.multiply(-1,cmdf)
    peaks = find_peaks(invCmdf,-th)
    if len(peaks[0]) > 0:
        sample = peaks[0][0]
    return sample

def YIN(noteData,fs,frames= 1470*2):
    fo = 0
    noteData = optimizeNote(noteData,frames)
    diff = differenceFunction(noteData,1/40,fs)
    #plt.plot(diff)
    #plt.show()
    cmdf = CMDF(diff) # ver lo de division por cero
    #plt.plot(cmdf)
    #plt.show()
    n = selectFoSample(cmdf)
    if n>0:
        fo = fs/n
    else: 
        fo = fs
    return fo

def freqToPitch(freq):
    return round(12*np.log2(freq/440)+69)

