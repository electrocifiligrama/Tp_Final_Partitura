#main program

from scipy.io import wavfile as wav
import segmentAlgorithms as SDA
import PDA as PDA
import OSS_generator as tempo #esto probablemente haya que cambiarlo
import frontend as front
from midiBuilder import MidiBuilder
import HarmPercSeparation as hp
#Funciones del main
def synthesize_wav():
    return
def spectrogram():
    return
def create_midi():
    # obtengo el audio monofónico
    AUDIO_PATH = ".\\Audios"
    INSTRUMENT = 1      # Grand Piano -- despues habria que agregar un diccionario si hace falta
    fileName = "punteoSongPiano"
    filePath = AUDIO_PATH + "\\" + fileName + ".wav"

    fs, audio = wav.read(filePath)
    audioMono = audio[:, 1]

    midi_filer = MidiBuilder(1000, INSTRUMENT)

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

def separate_harmonic_percussive():
    return

front.PrintInstructions()
selected_option = input()
#Realizo la accion correspondiente al input del usuario
if(selected_option == front.CREATE_MIDI):
    create_midi()
elif( selected_option == front.SYNTHESIZE_WAV):
    synthesize_wav()
elif( selected_option == front.SPECTROGRAM):
    spectrogram()
elif( selected_option == front.HARMONIC_PERCUSSIVE):
    hp.separate_harmonic_percussive()
else:
    #caso indefinido
    print("Opcion invalida\n")










