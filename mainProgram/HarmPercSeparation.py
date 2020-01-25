###########################################################################
#                           LIBRERIAS UTILIZADAS
###########################################################################
import SpectrumSeparator as sep
import scipy.io.wavfile as wa
import os

###########################################################################
#                               CONSTANTES
###########################################################################

WAV_PATH = ".\\Audios\\"


############################################################################
#                           FUNCIONES AUXILIARES
############################################################################


def isfloat(self,value):
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
    while not valid:
        frame_size_string = input("Ingrese la cantidad de muestras del audio utilizadas para realizar cada fft de la stft\n")
        result_str = IsValidNumber(frame_size_string)
        if(result_str =='Ok'):
            valid = True
            frame_size = int(frame_size_string)
        else:
            valid =False
            print("La opcion ingresada no es un numero positivo valido.\n")
    while not valid:
        beta_string = input("Ingrese el factor beta a utilizar en el algoritmo\n")
        result_str = IsValidNumber(frame_size_string)
        if(result_str =='Ok'):
            valid = True
            frame_size = int(frame_size_string)
        else:
            valid =False
            print("La opcion ingresada no es un numero positivo valido.\n")
#Obtiene los parametros del usuario a traves de la terminal
def GetUserData():
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
            if (num in midi_dict):
                valid =True
                file_name =  midi_dict[num]
        else:
            valid = False
            print(result_str)
    f_s, audio = wa.read(file_name)
    print("\nIngrese 'y' en caso afrimativo, en caso contrario ingrese cualquier otra tecla.\n")
    param_string = input("Desea configurar los parametros del algoritmo? (En caso contrario se usaran valores por default)\n")
    if( (param_string == 'y') or (param_string == 'Y') ):
        GetAlgorithmParams()



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
    t_h, audio_h, t_p, audio_p = sep.GetPercussiveAndHarmonicSpectrum() #Aplico el allgoritmo de separacion
    #Creo y guardo los archivos .wav nuevos.
    wa.write(file_name + "_armonico", f_s, audio_h)
    wa.write(file_name + "_percusivo", f_s, audio_p)