from scipy.io import wavfile as wav
from matplotlib import pyplot as plt
import numpy as np
import OSS_generator as o_gen
import BPM_FFT as b
from scipy import stats


def run(file_path, file_name, samples=750, n_fft=2048, alpha=0.85, desired_time=30):
    f_s, audio = wav.read(file_path)
    number_of_audios = 1
    if len(audio.shape) > 1:
        number_of_audios = 2
    bpm1 = []   # Bpm para el primer audio
    bpm2 = []   # Bpm del segundo audio (Solo se utiliza para audios en stereo)
    counter = 0
    bpm = 0
    detector = b.BPM_Detctor(n_fft, f_s, alpha)

    counter_limit = int(desired_time*f_s)

    while counter < counter_limit:
        stop = counter + samples
        if stop >= len(audio):
            stop = -1
        if number_of_audios > 1:
            buffer = audio[counter:stop, 0] / max(audio[:, 0])
            bpm = detector.BPM_estimate(buffer)
            bpm1.append(bpm)
        else:
            buffer = audio[counter:stop] / max(audio)
            bpm = detector.BPM_estimate(buffer)
            bpm1.append( bpm )
        counter += samples

    fig = plt.figure()
    t = np.linspace(start=0, stop=desired_time, num=len(bpm1))
    plt.plot(t, bpm1)
    plt.title("BPM de " + file_name)
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("BPM")
    # if number_of_audios > 1:
    #    plt.subplot(212)
    #    plt.plot(t,bpm2)
    plt.show()
    for i in range(0, len(bpm1)):
        bpm1[i] = int(round(bpm1[i]))
        # bpm2[i] = int(round(bpm2[i]))
    mode1, a = stats.mode(bpm1,axis=None)
    # mode2,a = stats.mode(bpm2,axis=None)
    print(mode1[0])
# print(mode2[0])


AUDIO_PATH = ".\\Audios\\"
file_name = "06-RunToTheHills.wav"
file_path = AUDIO_PATH + file_name
run(file_path=file_path, file_name=file_name)
