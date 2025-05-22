import numpy as np
from scipy.io.wavfile import read, write

if __name__ == '__main__':
    file1 = input("First file: ")
    file2 = input("Second file: ")
    outfile = input("Output file: ")

    blend_amount = float(input("Blend amount (0, 1): "))
    amp_mult = float(input("Amplitude multiplier (0, 1): "))

    assert 0 < blend_amount < 1

    rate1, data1 = read(file1)
    rate2, data2 = read(file2)

    assert rate1 == rate2

    avg1 = np.average(data1)
    avg2 = np.average(data2)

    min_size = min(len(data1), len(data2))
    result = (1 - blend_amount) * data1[:min_size] / avg1 * amp_mult + blend_amount * data2[:min_size] / avg2

    write(outfile, rate1, result)
