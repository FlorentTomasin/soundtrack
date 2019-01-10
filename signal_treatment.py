###############################
# Title: signal_treatment
# Author: Baptiste TOMASIN
###############################
"""
This py file you provides different functions to manipulate a sound signal:
    - Dysplay the spectrum of a sound
    - Find peaks in the spectrum
    - Determine coefficient between the amplitude of the fundamental frequency and its harmonics
    - Add harmonics to a pure sound
"""

###############################
# Imports
###############################
import pylab
import wavtool
import soundtrack_fibonacci

###############################
# Functions
###############################
def spectrum(S, freq):
    """
    This function generates the spectrum of the given 1D signal.

    S    : Table of the signal
    freq : Sample frequency
    """
    X=numpy.fft.fftshift(numpy.fft.fftfreq(len(S),1/freq))  # Frequency axis
    Y=numpy.fft.fftshift(abs(numpy.fft.fft(S)))             # FFT
    pylab.plot(X,Y)                                         # Display
    pylab.show()
    pylab.close()
    return

def detection_peak (frequency_axis,fft,n=300):
    """
    This function finds the peak in a spectrum for given 1D signal.

    It returns the list of peaks, the fundamental frequency and the
    list of peaks index.

    frequency_axis: Frequency axis of the spectrum
    fft           : fft of signal
    n             : Accuracy
    """
    fft[fft<fft.max()/1000]=0
    N=fft.shape[0]                            # Size of the fft
    fft=fft[:N//2]                            # Select the positive part of the fft
    frequency_axis=frequency_axis[:N//2]      # Select the positive part of the frequency
    window=[]                                 # Window to look into the fft
    Peak=[]                                   # List of the peaks' frequency
    Index_of_peak=[]                          # List of the peaks' index
    peak=0                                    # Index of harmonic
    m=0                                       # Harmonic value
    kcount=0                                  # Conter used to look into the fft

    while kcount!=len(fft)-n:
        window=fft[kcount:kcount+n]           # Select a part of the fft
        if m<window.max():
            m=window.max()
            peak=kcount+window.argmax()       # m index
        elif m>window.max():                  # if m>window.max() and window.max()==0, then m is an harmonic
            if window.max()==0:
                Peak+=[frequency_axis[peak]]
                Index_of_peak+=[peak]
                m=0
                peak=0
        kcount+=1
    fundamental_frequency=min(map(abs,Peak))

    return(Peak,fundamental_frequency,Index_of_peak)

def coef_timbre (sound):
    """
    This functin gives the list of the coefficients between the amplitude
    of the fundamental frequency and its harmonics.

    With the first value, the coeficient of the fundamental frequency,
    the second values the coeficient for the first harmonic...

    Sound : Sample sound you want to exract the timbre (1 fundamentale frequency)
    """
    signal,freq = wavtool.open_wav(sound)            # Signal: value of the sound
                                                     # Freq  : sample frequency
    frequency_axis = numpy.fft.fftfreq(len(signal),1/freq)
    fft = abs(numpy.fft.fft(signal))
    Peak,fundamental_frequency,Index_of_peak = detection_peak(frequency_axis,fft)
    kcount = 0                                       # Counter used to look into the fft
    Coef_timbre = []                                 # List of the coefficients
    indice_ff = Index_of_peak[0]                     # Index of the fundamental frequency
    harmonic_number = 0                              # Harmonic number

    while kcount != len(Peak):
        harmonic_number = round(Peak[kcount]/fundamental_frequency)
        while len(Coef_timbre) <= harmonic_number-2: # Add 0 if the frequence of the harmonic is not a Peak
            Coef_timbre += [0]
        indice = Index_of_peak[kcount]               # Index: index of the harmonic in fft
        coef = fft[indice]/fft[indice_ff]
        Coef_timbre+=[coef]
        kcount+=1
    return Coef_timbre                               # Return the list of coefficient

def apply_timbre (sound_signal, coef_timbre):
    """
    This function add harmonics to a pure sound.

    sound_signal: Table of sound
    coef_timbre : Coefficient of timbre
    """
    fft=abs(numpy.fft.fft(sound_signal))                          # fft of the signal
    fft=fft[:len(fft)//2]                                         # Select the positive part of the fft
    fft2=numpy.zeros((fft.shape[0]*2))                            # New fft
    ampli_ff = fft.max()                                          # Amplitude of the fundamental frequency
    index_ff=fft.argmax()                                         # Index of the fundamentale frequency
    for i in range (len(coef_timbre)):
        #if (i+1)*index_ff<len(fft2):
        fft2[(i+1)*index_ff]= ampli_ff * coef_timbre[i]           # Add harmonic in the positive part of the fft
        fft2[len(fft2)-(i+1)*index_ff]= ampli_ff * coef_timbre[i] # Add harmonic in the negative part of the fft
    return numpy.fft.ifft(fft2).real                              # Return the signal with harmonics

###############################
# Run
###############################
#soundtrack=generate_soundtrack(FNOTE, SAMPLE_RATE)
#wavtool.save_wav("output.wav", soundtrack, SAMPLE_RATE)
s = soundtrack_fibonacci.generate_sinewave(30000,3000,440,1,0)
s2=apply_timbre(s,coef_timbre("flute.wav"))
wavtool.save_wav("test.wav",s,30000)
spectrum(s2,30000)
