###############################
# Title: signal_treatment
# Author: Baptiste TOMASIN
###############################
"""
This py file provides different tools to manage the wav files:
    - Open a wav file and extract its sample rate
    - Save a signal in wav file

TODO: -function play
"""

###############################
# Imports
###############################
import wave
import struct
import numpy

###############################
# Functions
###############################
def open_wav(path):
    """
    Convert a WAV file to a 1D numpy float array and samples the frequency.
    It supportes only mono and only 8, 16 or 32 bits encoded WAV files.
    """
    w = wave.open(path, 'rb')
    samplewidth = w.getsampwidth()
    deltasample = [0, 1, 0, 0, 0]
    scalesample = [0, 127.5, 2 ** 15 - 1, 0, 2 ** 31 - 1]
    formatsample = ['', 'u1', '<i2', '', '<i4']
    t = numpy.fromstring(w.readframes(w.getnframes()), formatsample[samplewidth]).astype(float) / scalesample[samplewidth] - deltasample[samplewidth]
    samplefrequency = w.getframerate()
    return t, float(samplefrequency)

def save_wav(file_name, soundtrack, sample_rate):
    """
    This function all to save a soundtrack into a WAV audio file.
    """
    # Open a wav file
    wav_file=wave.open(file_name, "w")

    # wav params
    nchannels = 1
    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(soundtrack)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in soundtrack:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return
