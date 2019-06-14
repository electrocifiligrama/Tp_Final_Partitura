#main program

from scipy.io import wavfile as wav
import segmentAlgorithms as SDA
import PDA as PDA
import OSS_generator as tempo #esto probablemente haya que cambiarlo
import frontend as front

#obtengo el audio monofónico
AUDIO_PATH = ".\\Audios"

filePath = AUDIO_PATH + "\\kissSongPiano.wav"  
fs, audio = wav.read(filePath)
audioMono = audio[:, 1]

#tempo.detect(audioMono, fs)

#Se detectan los intervalos de tiempo donde predominan las notas musicales
noteSegments = SDA.notesSegmentation(audioMono, fs, SDA.HFC)

#Se averigua el pitch de las notas de cada intervalo hallado
notesFo = PDA.assignPitch(audioMono, fs, noteSegments, PDA.autocorrelationAlgorithm)

#A partir de la frecuencia fundamental de cada nota se averigua el nombre de las mismas 
notesName = PDA.translateNotes(notesFo)

#Se muestran gráficamente el resultado
front.showResults(notesName, noteSegments, audioMono)








