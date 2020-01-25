import scipy.signal as s
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wave
#Funcion que separa el espectro de un audio en dos espectros distintos.
#Un espectro corresponde a los sonidos harmonicos y otro a los percusivos.
#Recibe como parametros el arreglo con el audio, el largo de los filtros a aplicar,
#un factor beta que indica que tan exigente debe ser la separacion, y el tamano de frame
#que se desea para computar la STFT.
def GetPercussiveAndHarmonicSpectrum(input,h_filter_len=15,p_filter_len=15,frame_size=256,beta=3):

    #Largos de los filtros
    if( not(h_filter_len % 2) ):
        h_len =h_filter_len+1 #Defino el largo como impar
    else:
        h_len = h_filter_len
    if(not( p_filter_len % 2) ):
        p_len = p_filter_len+1 #Defino el largo como impar
    else:
        p_len = p_filter_len

    f,t,inp_spectr = s.stft(input,nperseg=frame_size)
    s_modules = np.abs( inp_spectr)

    #Aplico los filtros correspondientes para cada espectrograma
    h_filtered_spectr = np.zeros( (f.size,t.size) )
    p_filtered_spectr = np.zeros( (f.size,t.size) )

    for i in range(0,f.size): #Obtengo el espectro harmonico
        h_filtered_spectr[i] = s.medfilt(s_modules[i],h_len)
    for i in range(0,t.size): #Obtengo el espectro percusivo
        frame = s_modules[:,i]
        p_filtered_spectr[:,i] = s.medfilt(frame,p_len)
    #Genero las mascaras correspondientes
    Mask_h = np.zeros( (f.size,t.size),dtype='int16')
    Mask_p = np.zeros( (f.size,t.size),dtype='int16')
    for i in range(0,f.size):
        for j in range(0,t.size):
            Mask_h[i][j] = ( (h_filtered_spectr[i][j]/(p_filtered_spectr[i][j]+1e-10)) >= beta )
            Mask_p[i][j] = ( (p_filtered_spectr[i][j]/(h_filtered_spectr[i][j]+1e-10)) >= beta )
    #Consigo los espectros y los antitransformo
    h_spectr = np.multiply( inp_spectr,Mask_h)
    p_spectr = np.multiply( inp_spectr,Mask_p)
    t_h, audio_h = s.istft(h_spectr)
    t_p, audio_p = s.istft(p_spectr)
    return t_h, audio_h, t_p, audio_p

