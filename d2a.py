import numpy as np
import sounddevice as sd

from config import *
from utils import to_morse, DOT, DASH, SPACE

sd.default.samplerate = SAMPLE_RATE
sd.default.channels = 1


def sin_wave(duration):
    frames = int(duration * SAMPLE_RATE)
    t = np.arange(frames) / SAMPLE_RATE
    return AMPLITUDE * np.sin(2 * np.pi * FREQ * t)


def silence(duration):
    frames = duration * SAMPLE_RATE
    return np.zeros(int(frames))


class D2A:
    def __init__(self):
        self.wav = silence(1)

    def _add(self, wav: np.ndarray):
        self.wav = np.append(self.wav, wav)

    def encode(self, message: str):
        morse = to_morse(message)

        for char in morse:
            for sym in char:
                if sym == DOT:
                    self._add(sin_wave(DURATION))
                elif sym == DASH:
                    self._add(sin_wave(DASH_DURATION))
                elif sym == SPACE:
                    self._add(silence(SPACE_DURATION))
                self._add(silence(SYM_SPACER))
            self._add(silence(LETTER_SPACER))

    def play(self):
        print("Playing")
        sd.play(self.wav)
        sd.wait()

    def save(self, filename: str):
        from scipy.io.wavfile import write
        write(filename, SAMPLE_RATE, self.wav)

    def reset(self):
        self.wav = silence(1)

    def get_samples(self):
        return self.wav


if __name__ == '__main__':
    d2a = D2A()
    d2a.encode("Hello World")
    d2a.play()
