import time

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

from config import *
from goertzel import GoertzelSampleBySample

sd.default.samplerate = SAMPLE_RATE
sd.default.channels = 1


def _time_for_sample(sample):
    return sample / SAMPLE_RATE

class A2D:
    def __init__(self):
        self.message = ""
        self.times = []
        self.values = []
        self.sample_count = 0
        self.goertzel = GoertzelSampleBySample(FREQ, SAMPLE_RATE, GOERTZEL_SAMPLES)

    def _callback(self, indata: np.ndarray, frames: int,
                  time, status: sd.CallbackFlags):
        for i, sample in enumerate(indata):
            sample = sample[0]
            amplitude = self.goertzel.process_sample(sample) # Returns amplitude in dB
            if amplitude is not None:
                self.values.append(amplitude)
                self.times.append(_time_for_sample(self.sample_count + i))
                self.goertzel.reset()
        self.sample_count += len(indata)

    def read(self, filename: str):
        from scipy.io.wavfile import read
        rate, wav = read(filename)
        assert rate == SAMPLE_RATE

        for i, sample in enumerate(wav):
            amplitude = self.goertzel.process_sample(sample)
            if amplitude is not None:
                self.values.append(amplitude)
                self.times.append(_time_for_sample(self.sample_count + i))
                self.goertzel.reset()
        self.goertzel.reset()
        self.sample_count += len(wav)

    def record(self):
        with sd.InputStream(callback=self._callback, samplerate=SAMPLE_RATE, channels=1) as stream:
            self.goertzel.reset()
            input("Press Enter to stop...\n")
        self.goertzel.reset()

    def plot(self):
        plt.plot(self.times, self.values, marker='o')
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    a2d = A2D()
    a2d.read("Hello World noise.wav")
    a2d.plot()
