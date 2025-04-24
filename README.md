Dependencies (gensound):

```
pip install gensound
pip install -U --force git+https://github.com/cexen/py-simple-audio.git
```

Dependencies (sounddevice):
```
pip install sounddevice numpy scipy fastgoertzel
```

Convert a file to 16kHz mono: `ffmpeg -i <file> -ac 1 -ar 16000 <file.wav>`