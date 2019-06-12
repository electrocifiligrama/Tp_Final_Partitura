#HFC algorithm

import numpy as np
import math
import scipy.signal as signal 

def HFC(bufferIn,f_s=44100):
    
    k, n, Snn = signal.spectrogram(bufferIn, f_s)
    Nbins = len(k)
    Ntimes = len(n)
    En = np.zeros(Ntimes)

    for i in range(0, Ntimes-1):
        for j in range(0, Nbins-1):
            En[i] += (j*Snn[j, i])
        En[i] /= Nbins
 
    return En, n

def spectralDiff(bufferIn, f_s):
    k, n, Snn = signal.spectrogram(bufferIn, f_s)
    Nbins = len(k)
    Ntimes = len(n)
    SD = np.zeros(Ntimes)
    SD[0] = 0

    for i in range(1, Ntimes-1):
        for j in range(0, Nbins-1):
            SD[i] += ((Hx(Snn[j, i] - Snn[j, i-1]))**2)
    return SD, n



def Hx(x):
    return (x + abs(x))/2

    


