#main program

from scipy.io import wavfile as wav
import segmentAlgorithms as SDA
import PDA as PDA
import OSS_generator as tempo #esto probablemente haya que cambiarlo
import numpy as np

import matplotlib.pyplot as plt

#obtengo el audio monofónico
AUDIO_PATH = ".\\Audios"

filePath = AUDIO_PATH + "\\doMIsolDO.wav"  
fs, audio = wav.read(filePath)
audioMono = audio[:, 1]

#tempo.detect(audioMono, fs)

#Se detectan los intervalos de tiempo donde predominan las notas musicales
noteSegments = SDA.notesSegmentation(audioMono, fs, SDA.HFC)

#Se averigua el pitch de las notas de cada intervalo hallado
notesFo = PDA.assignPitch(audioMono, fs, noteSegments, PDA.YIN)


print(notesFo)







