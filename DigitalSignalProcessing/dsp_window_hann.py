#!/usr/bin/env python3

""" 音声情報処理 n本ノック !! """

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
# - ディジタルな正弦波を作成する
# - scipyのsignalモジュールでHann窓を作る
# - 定義式に従ってHann窓を作る

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

n_framerate = 2000            # 標本化周波数 (Hz)

freq = 20                     # 正弦波の周波数 (Hz)
duration = 1                  # 音の継続時間 (sec)
amplitude = 8000              # 正弦波の振幅

T = 1.0 / n_framerate         # 標本化周期 (sec)

# Hann窓の作成
WINDOW_LEN = 1025
hann_window = signal.hann(WINDOW_LEN)
hann_window_scratch = np.empty(WINDOW_LEN)
for n in range(WINDOW_LEN):
    hann_window_scratch[n] = 0.5 - 0.5 * \
        np.cos(2 * np.pi * n / (WINDOW_LEN - 1))

# scipyから作った窓関数と、定義式から作った窓関数をプロットして比較する
plt.plot(hann_window, label="scipy", linewidth=3)
plt.plot(hann_window_scratch, label="scratch")
plt.xlabel("Index")
plt.ylabel("Amplitude")
plt.title("Hann window")
plt.legend()
plt.show()

# 正弦波作成
time = np.arange(0, duration, T)  # 継続時間に等しい標本点の作成
sine_wave = amplitude * np.sin(2 * np.pi * freq * time)

# 正弦波に窓をかける
windowed = sine_wave[:WINDOW_LEN] * hann_window

# 正弦波のプロット
plt.plot(time[:WINDOW_LEN], sine_wave[:WINDOW_LEN], label="original")
plt.plot(time[:WINDOW_LEN], windowed, label="windowed")
plt.xlabel("Time (sec)")
plt.ylabel("Amplitude")
plt.title("Sine Wave")
plt.legend()
plt.show()
