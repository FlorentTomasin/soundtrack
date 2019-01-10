#!/usr/bin/env python
# coding: utf-8

###############################
# Title: Sound track generator
# Author: Baptiste TOMASIN
# Reviewer: Florent TOMASIN
###############################
"""
This algoritme aim to generates soundtrack following the Fibonacci serie.

Here are the documents and concept used to generate soundtrack using maths.

Useful links:
    1. https://www.easyzic.com/dossiers/la-gamme-de-pythagore,h151.html
    2. https://www.youtube.com/watch?v=IGJeGOw8TzQ

    The first link explains how to generate a diatonic scale so we can
    use to generate note sound.
    This scale is designed by Pythagore and can also be called
    "pure pythagoresque scale".

    The second link explain, how starting from the diatonic scale,
    we can generate a melody using the Fibonacci serie.

The frequential scale used is composed of 10 values (0 to 9).
Because we extract each number in the Fibonacci serie, we don't need more.

TODO:
    - Manage the note amplitude, time attenuation and period.
    - Currently all the notes have the same time length
      (time is one measure: (4 musical time) /4) and amplitude (equal to 1).
    - Generate specific instrument sound, like the piano, using the FFT/iFFT
      and filters.
"""

###############################
# Imports
###############################
import math
import random

###############################
# Globals
###############################
NB_NOTES_DIATONIC=8 # [do, ré, mi, fa, sol, la, si, do]
NOTE_DURATION=140   # Milliseconds
SAMPLE_RATE=44100.0 # Frequence of the sample rate
FNOTE=1*440.0       # Using La currently as a fundamental

###############################
# Functions
###############################
def init_diatonic_scale(fnote):
    """
    This function will generate the diatonic scale based on a given fundamental note.

    fnote: fundamental note.
    """
    n=0              # power value denumertor.
    jump=0           # index used to decide when jumping to another n.
    freq_scale=[]    # This Tab will include all the note of the diatonic scale.
    state=1          # 1: kcount 6, 2: kcount 1, 3: kcount 4.
    coef32=3.0 / 2.0 # Precompute this value to reduce CPU load.
    kcount=0         # counter used to switch from a state to another.
    tmp_note=0

    while len(freq_scale) < NB_NOTES_DIATONIC:
        tmp_note=fnote * ((coef32**len(freq_scale)) / (2.0**n))
        freq_scale=freq_scale+[tmp_note]

        if (state == 1):      # This state is used to compute 6 folloing values
            if (kcount == 5):
                state=2
                kcount=0
                jump=0
                n+=1
            else:
                if (jump==1):
                    n+=1
                    jump=0
                else:
                    jump+=1
                kcount+=1
        elif (state == 2):    # This state is used to compute 1 folloing values
            if (kcount == 0):
                state=3
                kcount=0
                jump=0
                n+=1
        elif (state == 3):    # This state is used to compute 4 folloing values
            if (kcount == 3):
                state=4
                kcount=0
                jump=0
                n+=1
            else:
                if (jump==1):
                    n+=1
                    jump=0
                else:
                    jump+=1
                kcount+=1
        elif (state == 4):    # This state is used to compute 1 folloing values
            if (kcount == 0):
                state=1
                kcount=0
                jump=0
                n+=1

    return (freq_scale)

def generate_sinewave(sample_rate, duration, freq, amplitude, phase):
    """
    Generate a sinusoidal signal at the given frequence for a given time.

    sample_rate: Defines the step between each sample of the track.
    duration:    Time length to play the note in millisecond.
    freq:        Number of pulses/samples per period.
    amplitude:   Amplitude of the signal.
    phase:       Phase of the signal.
    """
    wave=[]
    num_samples = duration * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        wave.append(amplitude * math.sin(2 * math.pi * freq * ( x / sample_rate ) + phase))

    return (wave)

def generate_soundtrack(fnote, sample_rate):
    """
    This function will generate a sound track by computing
    each notes following the Fibonacci serie.

    fnote:         Fundamental note used as base to generate the musical scale.
    sample_rate:   Defines the step between each sample of the track.
    """
    soundtrack=[]                # Tab of the samples composing the soundtrack.

    # Init frequential scale.
    freq_scale=init_diatonic_scale(fnote) # Init the musical diatonic scale according to the
                                          # given fundamental note.
    freq_scale=[freq_scale[6]]+freq_scale+[freq_scale[1]] # Add the first note of the previous octave and the
                                                          # first note of the next one. So the tab is size 10.

    # Generate the init sequence (mono-freq signals) and add it to the soundtrack.
    soundtrack+=generate_sinewave(sample_rate, NOTE_DURATION*random.uniform(0.8,2.0), freq_scale[0], random.uniform(0.8,1.0), 0.0) # Play the note 0 once.
    soundtrack+=generate_sinewave(sample_rate, NOTE_DURATION*random.uniform(0.8,2.0), freq_scale[1], random.uniform(0.8,1.0), 0.0) # Then play the note 1 once.
    soundtrack+=generate_sinewave(sample_rate, NOTE_DURATION*random.uniform(0.8,2.0), freq_scale[1], random.uniform(0.8,1.0), 0.0) # Then play the note 1 once.

    # Init Fibonacci serie
    Fn_2=1 # Fn-2 term of the Fibonacci serie.
    Fn_1=1*random.randint(1, 9) # Fn-1 term of the Fibonacci serie.
    Fn=0

    # while len(soundtrack) < samples:
    while Fn < 500:
        Fn=Fn_2+Fn_1      # Cumpute the Fibonacci serie.
        Fn_2,Fn_1=Fn_1,Fn # Swap/Shift the terms for the next loop.

        Fn_str=str(Fn)    # Convert to a string so we can extract each numbers individualy.

        for i in Fn_str:  # For each number, generate the signal of the associated note.
            soundtrack+=generate_sinewave(sample_rate, NOTE_DURATION*random.uniform(0.8,2.0), freq_scale[int(i)], random.uniform(0.6,1.0), 0.0)

    return (soundtrack)
