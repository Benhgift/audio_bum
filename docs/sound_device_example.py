import sounddevice as sd
import numpy as np

fs=44100
duration = 5  # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
print( "Recording Audio")
sd.wait()
print("rerd comple")
sd.play(myrecording, fs)
sd.wait()
print("play complete")
