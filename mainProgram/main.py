#main program

from scipy.io import wavfile as wav
import segmentAlgorithms as SDA
import PDA as PDA
import OSS_generator as tempo #esto probablemente haya que cambiarlo
import frontend as front
from midiBuilder import MidiBuilder
import HarmPercSeparation as hp
import GraphSpectrogram as gs
import os

AUDIO_PATH = ".\\Audios\\"

#Funciones del main

def isfloat(value):
      try:
        float(value)
        return True
      except ValueError:
        return False

#Valida que un string recibido sea un numero natural
def IsValidNumber(arg):
    if( isfloat(arg)): #valido el argumento
        arg_f=float(arg)
        if(arg_f<=0):
            return ( "El numero ingresado debe ser positivo\n")
        elif (arg_f==float("inf"))or(arg_f>=10e9):
            return ("El numero ingresado debe tener un valor finito\n")

    else:
        return ("Error de sintaxis\n")

    return "Ok" #El numero parece ser valido

def GetWavFileFromUser():
    valid = False
    i=0
    wav_dict = dict()
    for file in os.listdir(AUDIO_PATH):
        i +=1 
        if file.endswith(".wav"):
            print(str(i)+')'+file)
            wav_dict[i] = file
    while not valid:
        num_str = input("Por favor seleccione el .wav deseado ingresando el numero previo al nombre\n")
        result_str = IsValidNumber(num_str)
        if(result_str =='Ok'):
            num = int(num_str)
            if (num in wav_dict):
                valid =True
                file_name =  wav_dict[num]
        else:
            valid = False
            print(result_str)
    return file_name

def synthesize_wav():
    return
def spectrogram():
    return
def create_midi():
    # obtengo el audio monofónico 
    INSTRUMENT = 1      # Grand Piano -- despues habria que agregar un diccionario si hace falta
    fileName = "punteoSongPiano"
    filePath = AUDIO_PATH + fileName + ".wav"

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
    file_name = GetWavFileFromUser()
    gs.GraphSpectrogram( AUDIO_PATH + file_name)
elif( selected_option == front.HARMONIC_PERCUSSIVE):
    hp.separate_harmonic_percussive()
else:
    #caso indefinido
    print("Opcion invalida\n")










