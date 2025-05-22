import numpy as np

from config import *
from utils import to_morse, DOT, DASH, SPACE

class D2A:
    def __init__(self, sample_rate=SAMPLE_RATE, amplitude=AMPLITUDE):
        self.sample_rate = sample_rate
        self.amplitude = amplitude

        self.wav = self._silence(1)

    def _sin_wave(self, duration):
        frames = int(duration * self.sample_rate)
        t = np.arange(frames) / self.sample_rate
        return self.amplitude * np.sin(2 * np.pi * FREQ * t)

    def _silence(self, duration):
        frames = duration * self.sample_rate
        return np.zeros(int(frames))

    def _add(self, wav: np.ndarray):
        self.wav = np.append(self.wav, wav)

    def encode(self, message: str):
        morse = to_morse(message)

        for char in morse:
            for sym in char:
                if sym == DOT:
                    self._add(self._sin_wave(DURATION))
                elif sym == DASH:
                    self._add(self._sin_wave(DASH_DURATION))
                elif sym == SPACE:
                    self._add(self._silence(SPACE_DURATION))
                self._add(self._silence(SYM_SPACER))
            self._add(self._silence(LETTER_SPACER))

    def play(self):
        import sounddevice as sd
        print("Playing")
        sd.play(self.wav, samplerate=self.sample_rate)
        sd.wait()

    def save(self, filename: str):
        from scipy.io.wavfile import write
        write(filename, SAMPLE_RATE, self.wav)

    def reset(self):
        self.wav = self._silence(1)

    def get_samples(self):
        return self.wav


if __name__ == '__main__':
    d2a = D2A()
    message = input("Enter message: ").strip()
    d2a.encode(message)
    d2a.play()
