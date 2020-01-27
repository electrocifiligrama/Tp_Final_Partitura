###########################################################################
#                           LIBRERIAS UTILIZADAS
###########################################################################
import SpectrumSeparator as sep
import scipy.io.wavfile as wa
import os
import numpy as np

###########################################################################
#                               CONSTANTES
###########################################################################

WAV_PATH = ".\\Audios\\"


############################################################################
#                           FUNCIONES AUXILIARES
############################################################################


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

#Obtiene los parametros ya validados del algoritmo de separacion
def GetAlgorithmParams():
    valid = False
    frame_size = 0
    beta = 0
    h_len = 0
    p_len = 0
    while not valid:
        frame_size_string = input("Ingrese la cantidad de muestras del audio utilizadas para realizar cada fft de la stft\n")
        result_str = IsValidNumber(frame_size_string)
        if(result_str =='Ok'):
            valid = True
            frame_size = int(frame_size_string)
        else:
            valid =False
            print("La opcion ingresada no es un numero positivo valido.\n")
    valid = False
    while not valid:
        beta_string = input("Ingrese el factor beta a utilizar en el algoritmo\n")
        result_str = IsValidNumber(beta_string)
        if(result_str =='Ok'):
            valid = True
            beta = int(beta_string)
        else:
            valid =False
            print("La opcion ingresada no es un numero positivo valido.\n")
    valid = False
    while not valid:
        h_len_string = input("Ingrese la cantidad de muestras para el filtro armonico\n")
        result_str = IsValidNumber(h_len_string)
        if(result_str =='Ok'):
            valid = True
            h_len = int(h_len_string)
        else:
            valid =False
            print("La opcion ingresada no es un numero positivo valido.\n")
    valid = False
    while not valid:
        p_len_string = input("Ingrese la cantidad de muestras para el filtro percusivo\n")
        result_str = IsValidNumber(p_len_string)
        if(result_str =='Ok'):
            valid = True
            p_len = int(p_len_string)
        else:
            valid =False
            print("La opcion ingresada no es un numero positivo valido.\n")
    return frame_size, beta, h_len, p_len
#Obtiene los parametros del usuario a traves de la terminal
def GetUserData():
    valid = False
    i=0
    wav_dict = dict()
    for file in os.listdir(WAV_PATH):
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
    f_s, audio = wa.read( WAV_PATH + file_name)
    print("\nIngrese 'y' en caso afrimativo, en caso contrario ingrese cualquier otra tecla.\n")
    param_string = input("Desea configurar los parametros del algoritmo? (En caso contrario se usaran valores por default)\n")
    if( (param_string == 'y') or (param_string == 'Y') ):
        frame_size, beta, h_len, p_len = GetAlgorithmParams()
    else:   #Uso parametros por default
        frame_size = 1024
        beta = 3
        h_len = 15
        p_len = 15
    return file_name, f_s, audio, h_len, p_len, beta, frame_size

def PrintInstructions():
    print("El siguiente programa recibe un archivo de audio .wav y lo procesa con el fin de generar\n")
    print("otros dos archivos .wav.En uno de dichos archivos se encuentran solo los elementos armonicos\n")
    print("del audio, mientras que en el segundo solo se encuentran los elementos percusivos del mismo.\n")



############################################################################
#                           FUNCION PRINCIPAL
############################################################################


#Funcion que se encarga de generar dos archivos .wav a partir
#de un archivo .wav seleccionado. En uno de los archivos generados
#se guardan unicamente los sonidos percusivo del .wav seleccionado
#mientras que en el otro se guardan solo los sonidos armonicos.
def separate_harmonic_percussive():

    PrintInstructions()  #Explico al usuario la funcionalidad del programa y muestro
                         #los .wav posibles para elegir
    file_name, f_s, audio, h_len, p_len, beta, frame_size = GetUserData() #Obtengo los parametros deseados del usuario.
    if(  len(audio.shape) == 1 ):   #Audio en mono
        t_h, audio_h, t_p, audio_p = sep.GetPercussiveAndHarmonicSpectrum(audio, h_len, p_len, frame_size, beta) #Aplico el allgoritmo de separacion
        wa.write(file_name + "_armonico", f_s, audio_h)
        wa.write(file_name + "_percusivo", f_s, audio_p)
    else:   #Audio en estereo
        audio1 = audio[:,0]
        audio2 = audio[:,1]
        t_h1, audio_h1, t_p1, audio_p1 = sep.GetPercussiveAndHarmonicSpectrum(audio1, h_len, p_len, frame_size, beta) #Aplico el allgoritmo de separacion
        t_h2, audio_h2, t_p2, audio_p2 = sep.GetPercussiveAndHarmonicSpectrum(audio2, h_len, p_len, frame_size, beta) #Aplico el allgoritmo de separacion
        #Guardo la parte armonica
        audio_aux = np.zeros( audio.shape, audio.dtype)
        audio_aux[:,0] = audio_h1[:len( audio_aux[:,0] )]
        audio_aux[:,1] = audio_h2[:len( audio_aux[:,0] )]
        wa.write(WAV_PATH + "armonico_" + file_name, f_s, audio_aux)
        #Guardo la parte percusiva
        audio_aux[:,0] = audio_p1[:len( audio_aux[:,0] )]
        audio_aux[:,1] = audio_p2[:len( audio_aux[:,0] )]
        wa.write(WAV_PATH + "percusivo_"+ file_name, f_s, audio_aux)