import traceback

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import fastgoertzel as G

from config import *
from utils import to_morse, DOT, DASH, SPACE

sd.default.samplerate = SAMPLE_RATE
sd.default.channels = 1

class ADC:
    def __init__(self):
        self.message = ""
        self.morse = []

    def _callback(self, indata: np.ndarray, frames: int,
         time, status: sd.CallbackFlags):
        data = np.zeros(frames)
        np.copyto(data, indata.ravel())
        try:
            amp, phase = G.goertzel(data, SAMPLE_RATE / FREQ)
            print(amp, phase)
        except:
            traceback.print_exc()


    def record_and_decode(self):
        with sd.InputStream(callback=self._callback, samplerate=SAMPLE_RATE, channels=1, blocksize=16000) as stream:
            input("Press Enter to stop...")

if __name__ == '__main__':
    adc = ADC()
    adc.record_and_decode()