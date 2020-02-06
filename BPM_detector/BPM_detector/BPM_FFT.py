import numpy as np
import math
import scipy.signal as sig 
from matplotlib import pyplot as plt
MINIMUM_F= 1
MAXIMUM_F = 3

class BPM_Detctor(object):
    """Clase que se encarga de detectar el BPM de una cancion"""
    def __init__(self, number_of_frames =2048,f_s=44100,alpha_ =0.8):
        self.power = np.zeros(number_of_frames)
        self.nfft = number_of_frames
        #Circular array indexes
        self.curr = 0
        self.overflow = False
        self.fs = f_s
        self.alpha = alpha_

    def BPM_estimate(self, buffer):
        buffer_size = len(buffer)
        if( self.overflow):
            self.power = np.delete(self.power,0)
            self.power = np.append(self.power,0)
        average = ( sig.fftconvolve(buffer,buffer[::-1])[0] )/ buffer_size
        self.power[self.curr] = self.alpha*(self.power[self.curr - 1]) + (1-self.alpha)*average
        fs_nueva = self.fs/buffer_size    
        power_spectrum = np.abs( np.fft.rfft(self.power,n=self.nfft) )
        #f = np.linspace(start=0,stop=fs_nueva/2.0,num=len( power_spectrum))
        #plt.plot(f,power_spectrum)
        #plt.show()
        rfft_size = len(power_spectrum)
        freq_res = fs_nueva/(2*rfft_size)
        bin_start = int( round(MINIMUM_F/freq_res) )
        bin_stop = int( round(MAXIMUM_F/freq_res) )
        bin_max = bin_start + np.argmax(power_spectrum[bin_start:bin_stop])
        f_max = bin_max*freq_res

        #Actualizo indices
        if ( (self.curr + 1) == self.nfft ):
            self.overflow = True
        else:
            self.curr = self.curr + 1

        return (f_max*60)

