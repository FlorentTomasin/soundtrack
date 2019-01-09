###############################
# Title: signal_treatment
# Author: Baptiste TOMASIN
###############################
'''
In this files you can find different function to manipulate a sound signal, like :
    - dysplay the spectrum of a sound
    - find peaks in spectrum
    - determine coefficient between the amplitude of the fundamental frequency and its harmonics
    - add harmonics to pure sound
    
'''

###############################
# Imports
###############################
import numpy
import pylab
import wavtool
import soundtrack_fibonacci

###############################
# Functions
###############################
def spectrum(S, freq):
    '''
    This genere the spectrum of a 1D signal
    
    S : table of the signal
    
    freq : sample frequency 
    
    '''
    X=numpy.fft.fftshift(numpy.fft.fftfreq(len(S),1/freq))  #frequency axis
    Y=numpy.fft.fftshift(abs(numpy.fft.fft(S)))             #fft
    pylab.plot(X,Y)                                         #display
    pylab.show()
    pylab.close()
    return

def detection_peak (frequency_axis,fft,n=300):
    """
    This find peak in a spectrum for 1D signal
    
    frequency_axis: frequency axis of the spectrum
    fft: fft of signal
    n: accuracy
    """
    
    fft[fft<fft.max()/1000]=0                 
    N=fft.shape[0]                            #size of the fft
    fft=fft[:N//2]                            #select the positive part of the fft
    frequency_axis=frequency_axis[:N//2]      #select the positive part of the frequency
    window=[]                                 #window to look into the fft
    Peak=[]                                   #list of the peaks' frequency
    Index_of_peak=[]                          #list of the peaks' index
    peak=0                                    #index of harmonic
    m=0                                       #harmonic value
    kcount=0                                  #conter used to look into the fft
    
    
    while kcount!=len(fft)-n:                
        window=fft[kcount:kcount+n]          #select a part of the fft
        if m<window.max():
            m=window.max()
            peak=kcount+window.argmax()     #m index
        elif m>window.max():                #if m>window.max() and window.max()==0, so m is an harmonic
            if window.max()==0:             
                Peak+=[frequency_axis[peak]]
                Index_of_peak+=[peak]
                m=0
                peak=0
        kcount+=1
    fundamental_frequency=min(map(abs,Peak))
    
    return(Peak,fundamental_frequency,Index_of_peak) #return the list of peak, the fundamental frequnency and the list of peaks' index

def coef_timbre (sound):
    """
    This give the list of coefficient between the amplitude of the fundamental frequency and its harmonics
    With the first value, the coeficient of the fundamental frequency, the second values the coeficient for the first harmonic...

    Sound : sample sound where you desire the timbre (1 fundamentale frequency)    
    
    """
    
    signal,freq = wavtool.open_wave(sound)                                         #signal: value of the sound
                                                                                   #freq: sample frequency
    frequency_axis = numpy.fft.fftfreq(len(signal),1/freq)
    fft = abs(numpy.fft.fft(signal))
    Peak,fundamental_frequency,Index_of_peak = detection_peak(frequency_axis,fft)
    kcount = 0                                                                     #conter used to look into the fft
    Coef_timbre = []                                                               #list of the coefficient
    indice_ff = Index_of_peak[0]                                                   #index of the fundamental frequency
    harmonic_number = 0                                                            #harmonic number

    while kcount != len(Peak):                                                     
        harmonic_number = round(Peak[kcount]/fundamental_frequency)                
        while len(Coef_timbre) <= harmonic_number-2:                               #add 0 if the frequence of harmonic is not in Peak
            Coef_timbre += [0]
        indice = Index_of_peak[kcount]                                             #index: index of the harmonic in fft
        coef = fft[indice]/fft[indice_ff]
        Coef_timbre+=[coef]
        kcount+=1
    return Coef_timbre                                                             #return the list of coefficient

def apply_timbre (sound_signal, coef_timbre):
    '''
    This add harmonics to pure sound

    sound_signal: table of sound 
    coef_timbre: coefficient of timbre
    
    '''
    
    fft=abs(numpy.fft.fft(sound_signal))                            #fft of the signal
    fft=fft[:len(fft)//2]                                           #select the positive part of the fft
    fft2=numpy.zeros((fft.shape[0]*2))                              #new fft
    ampli_ff = fft.max()                                            #amplitude of the fundamental frequency
    index_ff=fft.argmax()                                           #index of the fundamentale frequency
    for i in range (len(coef_timbre)):
        #if (i+1)*index_ff<len(fft2):
        fft2[(i+1)*index_ff]= ampli_ff * coef_timbre[i]             #add harmonic in the positive part of fft
        fft2[len(fft2)-(i+1)*index_ff]= ampli_ff * coef_timbre[i]   #add harmonic in the negative part of fft
    return numpy.fft.ifft(fft2).real                                #return the signal with harmonic

s = soundtrack_fibonacci.generate_sinewave(30000,3000,440,1,0)
s2=apply_timbre(s,coef_timbre("flute.wav"))
wavtool.save_wav("test.wav",s,30000)
spectrum(s2,30000)
