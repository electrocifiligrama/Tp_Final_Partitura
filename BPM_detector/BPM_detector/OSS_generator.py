import numpy as np
import math
import scipy.signal as sig 
from matplotlib import pyplot as plt
def GenerateOSS(buffer,f_s=44100,window_=None,hop_size=128,n_fft=1024):
    window = window_
    if window == None:
        window = np.hamming(n_fft)
    window_size = window.size
    buffer_size = len(buffer)
    number_of_frames = math.ceil( buffer_size/hop_size )
    if( n_fft % 2): #Si n es impar entonces la r_fft devuelve (n+1)/2 valores
        rfft_size = (n_fft+1)/2
    else:
        rfft_size = (n_fft/2)+1
    log_power = np.zeros( shape=(number_of_frames,int(rfft_size)))
    flux = np.zeros(number_of_frames)
    for i in range(0,number_of_frames):
        start_index= i*hop_size
        stop_index= start_index+window_size
        if(stop_index >= buffer_size):
            stop_index=-1
        frame = np.array( buffer[start_index:stop_index] )  #Tomo un numero de muestras del audio
        if len(frame < window_size):
            frame = np.append( frame,np.zeros(int(window_size-frame.size)))
        windowed_frame = np.multiply(frame,window)  #y les aplico la funcion ventana.
        #Le aplico la fft al frame ventaneado
        frame_spectrum = np.fft.rfft(windowed_frame,n=n_fft)
        #Calculo la potencia logaritmica
        log_power[i] = np.log(1+ 1000*np.abs(frame_spectrum))
        #Aplico la formula de Flux
        for j in range(1,frame_spectrum.size):
            power_change = log_power[i][j] - log_power[i-1][j]
            if power_change > 0:
                flux[i] += power_change
        
    #Genero y aplico un filtro pasabanda a la salida
    filter_order = 15
    f_s_oss = f_s/hop_size
    f_c = 4 #Frecuencia de corte correspondiente a 240 BPM
    h = sig.firwin(numtaps=filter_order+1,cutoff=f_c,fs=f_s_oss)
    #f = np.linspace(start=0,stop=f_s_oss/2.0,num=len(flux_spectrum))
    #plt.plot(f,flux_spectrum)
    #plt.show()
    flux = np.convolve(flux,h)
    return flux

