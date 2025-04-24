import time

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

from config import *
from goertzel import GoertzelSampleBySample

sd.default.samplerate = SAMPLE_RATE
sd.default.channels = 1


class A2D:
    def __init__(self):
        self.message = ""
        self.times = []
        self.values = []
        self.sample_count = 0
        self.goertzel = GoertzelSampleBySample(FREQ, SAMPLE_RATE, 128)

    def _callback(self, indata: np.ndarray, frames: int,
                  time, status: sd.CallbackFlags):
        for i, sample in enumerate(indata):
            sample = sample[0]
            amplitude = self.goertzel.process_sample(sample) # Returns amplitude in dB
            if amplitude is not None:
                self.values.append(amplitude)
                self.times.append((self.sample_count + i) / SAMPLE_RATE)
                self.goertzel.reset()
        self.sample_count += len(indata)

    def record_and_decode(self):
        with sd.InputStream(callback=self._callback, samplerate=SAMPLE_RATE, channels=1) as stream:
            input("Press Enter to continue...\n")

    def plot(self):
        plt.plot(self.times, self.values, marker='o')
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    a2d = A2D()
    a2d.record_and_decode()
    a2d.plot()
