import numpy as np

from config import *
from goertzel import GoertzelSampleBySample
from utils import DOT, DASH, SPACE, from_morse


class A2D:
    def __init__(self, sample_rate=SAMPLE_RATE):
        self.sample_rate = sample_rate

        self.times = []
        self.values = []
        self.sample_count = 0
        self.goertzel = GoertzelSampleBySample(FREQ, SAMPLE_RATE, GOERTZEL_SAMPLES)

    def _time_for_sample(self, sample):
        return sample / self.sample_rate

    def _inject(self, samples):
        for i, sample in enumerate(samples):
            amplitude = self.goertzel.process_sample(sample)  # Returns amplitude in dB
            if amplitude is not None:
                self.values.append(amplitude)
                self.times.append(self._time_for_sample(self.sample_count + i))
                self.goertzel.reset()
        self.sample_count += len(samples)

    def _callback(self, indata: np.ndarray, frames: int,
                  time, status):
        self._inject(indata.flat)

    def read(self, filename: str):
        from scipy.io.wavfile import read
        rate, wav = read(filename)
        assert rate == SAMPLE_RATE

        self._inject(wav)

    def read_samples(self, samples):
        self._inject(samples)

    def record(self):
        import sounddevice as sd
        with sd.InputStream(callback=self._callback, samplerate=self.sample_rate, channels=1) as stream:
            self.goertzel.reset()
            print("Recording")
            input("Press Enter to stop...\n")
        self.goertzel.reset()

    def decode(self):
        max_amp = float(np.max(self.values))
        avg_amp = float(np.average(self.values))

        eps = 10

        # Segment the values into rising, falling and flat times

        FALLING = "falling"
        RISING = "rising"
        FLAT = "flat"

        state = RISING
        last_start = 0

        segments = []

        start_index = 0
        val = self.values[start_index]
        while val < avg_amp:
            start_index += 1
            val = self.values[start_index]
            last_start = self.times[start_index - 1]

        for i in range(start_index, len(self.values)):
            last_val = self.values[i - 1]
            val = self.values[i]
            t = self.times[i]

            if val > last_val + eps:
                if state != RISING:
                    segments.append((state, t - last_start))
                    state = RISING
                    last_start = t
            elif val + eps < last_val:
                if state != FALLING:
                    segments.append((state, t - last_start))
                    state = FALLING
                    last_start = t
            else:
                if state != FLAT:
                    segments.append((state, t - last_start))
                    state = FLAT
                    last_start = t

        segments_high_low = []

        # Turn segments into high and low times
        high_time = 0
        low_time = 0
        is_rising = False
        for state, t in segments:
            if state == RISING:
                if not is_rising:
                    is_rising = True
                    segments_high_low.append((False, low_time))
                    low_time = 0
                    high_time = t
            if state == FALLING:
                if is_rising:
                    is_rising = False
                    segments_high_low.append((True, high_time))
                    high_time = 0
                    low_time = 0

            if is_rising:
                high_time += t
            else:
                low_time += t

        print(segments)
        print(segments_high_low)

        # Turn segments into dots and dashes
        morse = []
        current_letter = []
        for is_high, time in segments_high_low:
            if is_high:
                if time < (DURATION + DASH_DURATION) / 2:
                    current_letter.append(DOT)
                else:
                    current_letter.append(DASH)
            else:
                if time < (SYM_SPACER + LETTER_SPACER) / 2:
                    continue  # symbol spacer
                elif time < (LETTER_SPACER + SPACE_DURATION) / 2:
                    morse.append(current_letter)
                    current_letter = []
                else:
                    # space
                    if len(current_letter) > 0:
                        morse.append(current_letter)
                        current_letter = []
                    morse.append([SPACE])
        if len(current_letter) > 0:
            morse.append(current_letter)

        return from_morse(morse)

    def plot(self):
        import matplotlib.pyplot as plt
        max_amp = float(np.max(self.values))
        avg_amp = float(np.average(self.values))
        high = (max_amp + avg_amp) / 2

        first = 0
        for i, v in enumerate(self.values):
            if v > high:
                first = i
                break

        last = len(self.values)
        for i in range(len(self.values), first, -1):
            if self.values[i - 1] > high:
                last = i
                break

        values = self.values[first:last]
        times = self.times[first:last]

        plt.plot(times, values, marker='o')
        plt.grid(True)
        plt.show()

    def reset(self):
        self.values = []
        self.times = []
        self.sample_count = 0
        self.goertzel.reset()


if __name__ == '__main__':
    a2d = A2D()
    a2d.record()
    # a2d.read("Hello.wav")
    print(a2d.decode())
    a2d.plot()
