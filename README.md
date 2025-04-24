Dependencies:

```
pip install sounddevice numpy scipy
```

If you want to read from file, you need to convert it to the target sample rate.
Convert a file to 16kHz mono: `ffmpeg -i <file> -ac 1 -ar 16000 <file.wav>`

You can set the duration of a dot, the frequency, and the sample rate in `config.py`.