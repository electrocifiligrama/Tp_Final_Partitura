#frontend

import numpy as np
from matplotlib import pyplot as plt

#Defines
CREATE_MIDI = 1
SYNTHESIZE_WAV = 2
SPECTROGRAM = 3
HARMONIC_PERCUSSIVE = 4


def showResults(notesName, noteSegments, audioMono):
    frames = np.arange(0, len(audioMono), 1)
    plt.figure()
    plt.title("Resultados Obtenidos - Entrada Original Vs Notas Detectadas")
    plt.xlabel("tiempo (segundos)")
    plt.ylabel("Magnitud de Señal de Audio")
    plt.plot(frames, audioMono)  #Se grafica la señal de audio original
    

    for i in range(0, len(noteSegments[:, 0])):
        plt.axvline(x = noteSegments[i][0], clip_on = True, color = 'r') #Se marcan los onsets
        plt.axvline(x = noteSegments[i][1], clip_on = True, color = 'g') #Se marcan los offsets
        plt.text(noteSegments[i][0], 0, notesName[i]) #Se indica el nombre de las notas al comienzo de cada nota (en los onsets)

    plt.show()
    
def PrintInstructions():
    print("El siguiente programa tiene distintas funcionalidades todas relacionadas a la manipulacion de archivos\n")
    print("de audio .wav como de archivos MIDI.\n")
    print("Eliga la opcion deseada apretando en el terclado el numero que precede a la misma:")
    #Listado de opciones que realiza el programa
    print("1) Obtener el midi a partir de un .wav\n")
    print("2) Obtener .wav a partir de un midi\n")
    print("3) Ver el espectrograma de un audio\n")
    print("4) Separar un .wav en su parte percusiva y su parte armonica\n")



