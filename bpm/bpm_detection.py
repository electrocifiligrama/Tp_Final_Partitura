# https://github.com/scaperot/the-BPM-detector-python

# Copyright 2012 Free Software Foundation, Inc.
#
# This file is part of The BPM Detector Python
#
# The BPM Detector Python is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# The BPM Detector Python is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with The BPM Detector Python; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

import wave, array, math, time, argparse, sys
import numpy, pywt
from scipy import signal
import pdb
import matplotlib.pyplot as plt


AUDIO_PATH = ".\\Audios"
file_path = AUDIO_PATH + "\\clicktrack80bpm.wav"


def read_wav(filename):

    # open file, get metadata for audio
    try:
        wf = wave.open(filename, "rb")
    except IOError as e:
        print(e)
        return

    # typ = choose_type( wf.getsampwidth() ) #TODO: implement choose_type
    nsamps = wf.getnframes()
    assert nsamps > 0

    fs = wf.getframerate()
    assert fs > 0

    # read entire file and make into an array
    samps = list(array.array("i", wf.readframes(nsamps)))
    # print('Read', nsamps,'samples from', filename)
    try:
        assert nsamps == len(samps)
    except AssertionError as e:
        print(nsamps, "not equal to", len(samps))

    return samps, fs


# print an error when no data can be found
def no_audio_data():
    print("No audio data for sample, skipping...")
    return None, None


# simple peak detection
def peak_detect(data):
    max_val = numpy.amax(abs(data))
    peak_ndx = numpy.where(data == max_val)
    if len(peak_ndx[0]) == 0:  # if nothing found then the max must be negative
        peak_ndx = numpy.where(data == -max_val)
    return peak_ndx


def bpm_detector(data, fs):
    cA = []
    cD = []
    correl = []
    cD_sum = []
    levels = 4
    max_decimation = 2 ** (levels - 1)
    min_ndx = math.floor(60.0 / 220 * (fs / max_decimation))
    max_ndx = math.floor(60.0 / 40 * (fs / max_decimation))

    for loop in range(0, levels):
        cD = []
        # 1) DWT
        if loop == 0:
            [cA, cD] = pywt.dwt(data, "db4")
            cD_minlen = len(cD) / max_decimation + 1
            cD_sum = numpy.zeros(math.floor(cD_minlen))
        else:
            [cA, cD] = pywt.dwt(cA, "db4")

        # 2) Filter
        cD = signal.lfilter([0.01], [1 - 0.99], cD)

        # 4) Subtractargs.filename out the mean.

        # 5) Decimate for reconstruction later.
        cD = abs(cD[:: (2 ** (levels - loop - 1))])
        cD = cD - numpy.mean(cD)

        # 6) Recombine the signal before ACF
        #    essentially, each level I concatenate
        #    the detail coefs (i.e. the HPF values)
        #    to the beginning of the array
        cD_sum = cD[0 : math.floor(cD_minlen)] + cD_sum

    if [b for b in cA if b != 0.0] == []:
        return no_audio_data()
    # adding in the approximate data as well...
    cA = signal.lfilter([0.01], [1 - 0.99], cA)
    cA = abs(cA)
    cA = cA - numpy.mean(cA)
    cD_sum = cA[0 : math.floor(cD_minlen)] + cD_sum

    # ACF
    correl = numpy.correlate(cD_sum, cD_sum, "full")

    midpoint = math.floor(len(correl) / 2)
    correl_midpoint_tmp = correl[midpoint:]
    peak_ndx = peak_detect(correl_midpoint_tmp[min_ndx:max_ndx])
    if len(peak_ndx) > 1:
        return no_audio_data()

    peak_ndx_adjusted = peak_ndx[0] + min_ndx
    bpm = 60.0 / peak_ndx_adjusted * (fs / max_decimation)
    print(bpm)
    return bpm, correl


def run(filename, window=3.0):
    """
    :param filename: .wav file for processing
    :param window: size of the the window (seconds) that will be scanned to determine the bpm.  Typically less than 10 seconds. [3]
    :return: None
    """

    samps, fs = read_wav(filename)

    data = []
    correl = []
    bpm = 0
    n = 0
    nsamps = len(samps)
    window_samps = int(window * fs)
    samps_ndx = 0  # first sample in window_ndx
    max_window_ndx = math.floor(nsamps / window_samps)
    bpms = numpy.zeros(max_window_ndx)

    # iterate through all windows
    for window_ndx in range(0, max_window_ndx):

        # get a new set of samples
        # print(n,":",len(bpms),":",max_window_ndx_int,":",fs,":",nsamps,":",samps_ndx)
        data = samps[samps_ndx : samps_ndx + window_samps]
        if not ((len(data) % window_samps) == 0):
            raise AssertionError(str(len(data)))

        bpm, correl_temp = bpm_detector(data, fs)
        if bpm is None:
            continue
        bpms[window_ndx] = bpm
        correl = correl_temp

        # iterate at the end of the loop
        samps_ndx = samps_ndx + window_samps
        n = n + 1
        # counter for debug...

    bpm = numpy.median(bpms)
    print("Completed.  Estimated Beats Per Minute:", bpm)

    n = range(0, len(correl))
    plt.plot(n, abs(correl))
    plt.show(block=True)


run(filename=file_path, window=3.0)
