#frontend

import numpy as np
from matplotlib import pyplot as plt

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
    


