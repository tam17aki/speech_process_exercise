#!/usr/bin/env python3

# MIT License

# Copyright (C) 2020 by Akira TAMAMORI

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Commentary:
# DIO による基本周波数推定

import matplotlib.pyplot as plt
import numpy as np
import pyworld
from scipy.io import wavfile

IN_WAVE_FILE = "in.wav"
FRAME_LENGTH = 1024  # フレーム長 (FFTサイズ)
HOP_LENGTH = 80  # フレームのシフト長

# 音声のロード
fs, data = wavfile.read(IN_WAVE_FILE)
data = data.astype(np.float64)

# DIO に基づく基本周波数推定
fo, _ = pyworld.dio(data, fs)

# 波形表示
fig = plt.figure(figsize=(12, 6))
n_samples = len(data)
time = np.arange(n_samples) / fs
axes = fig.add_subplot(2, 1, 1)
axes.plot(time, data)
axes.set_xlabel("Time (sec)")
axes.set_ylabel("Amplitude")
axes.set_title("Waveform")
axes.set_xlim(0, np.max(time))

axes = fig.add_subplot(2, 1, 2)
axes.plot(fo)
axes.set_xlabel("Frame number")
axes.set_ylabel("Frequency (Hz)")
axes.set_title("Estimation of fundamental frequency via pYIN method")
axes.set_xlim(0, len(fo) - 1)

plt.tight_layout()
plt.show()
