#main program

from scipy.io import wavfile as wav
import segmentAlgorithms as SDA
import PDA as PDA
import OSS_generator as tempo #esto probablemente haya que cambiarlo
import frontend as front
from midiBuilder import MidiBuilder

# obtengo el audio monofónico
AUDIO_PATH = ".\\Audios"
fileName = "punteoSongPiano"
filePath = AUDIO_PATH + "\\" + fileName + ".wav"

fs, audio = wav.read(filePath)
audioMono = audio[:, 1]

midi_filer = MidiBuilder(1000)

# tempo.detect(audioMono, fs)

# Se detectan los intervalos de tiempo donde predominan las notas musicales
noteSegments = SDA.notesSegmentation(audioMono, fs, SDA.HFC)

# Se averigua el pitch de las notas de cada intervalo hallado
notesFo = PDA.assignPitch(audioMono, fs, noteSegments, PDA.autocorrelationAlgorithm)

# A partir de la frecuencia fundamental de cada nota se averigua el nombre de las mismas
notesName = PDA.translateNotes(notesFo)

# Se genera el archivo midi correspondiente para corroborar que se detectaron las notas correctamente
midi_filer.play_notes(noteSegments, fs, notesFo, fileName)

# Se muestran gráficamente el resultado
front.showResults(notesName, noteSegments, audioMono)








