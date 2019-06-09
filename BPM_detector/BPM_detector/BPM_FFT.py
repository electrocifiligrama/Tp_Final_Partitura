import numpy as np
import math
import scipy.signal as sig 
from matplotlib import pyplot as plt
MINIMUM_F= 1
MAXIMUM_F = 3
def BPM_estimate(buffer,f_s=44100,n_samples=280,alpha=0.8):
    buffer_size = len(buffer)
    number_of_frames = math.ceil( buffer_size/n_samples )
    n_fft = int(2*number_of_frames)
    if( n_fft % 2): #Si n es impar entonces la r_fft devuelve (n+1)/2 valores
        rfft_size = (n_fft+1)/2
    else:
        rfft_size = (n_fft/2)+1
    frame = buffer[0:n_samples]
    power = np.zeros(number_of_frames)
    power[0] = (1-alpha)*sig.fftconvolve(frame,frame[:-1])[0]
    power[0] /= n_samples
    for i in range(1,number_of_frames):
        start_index = i*n_samples
        stop_index = (i+1)*n_samples
        if stop_index >= len(buffer):
            stop_index = -1
        frame = buffer[start_index:stop_index]
        #Calculo la potencia
        frame_average = sig.fftconvolve(frame,frame[:-1])[0]
        frame_average /= len(frame)
        power[i] = alpha*(power[i-1]) + (1-alpha)*frame_average
    fs_nueva = f_s/n_samples    
    power_spectrum = np.abs( np.fft.rfft(power,n=n_fft) )
    #f = np.linspace(start=0,stop=fs_nueva/2.0,num=len( power_spectrum))
    #plt.plot(f,power_spectrum)
    #plt.show()
    freq_res = fs_nueva/(n_fft)
    bin_start = int( round(MINIMUM_F/freq_res) )
    bin_stop = int( round(MAXIMUM_F/freq_res) )
    bin_max = bin_start + np.argmax(power_spectrum[bin_start:bin_stop])
    f_max = bin_max*freq_res

    return (f_max*60)

