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
# - オイラーの公式により複素正弦波を作成する
# - 複素数の実部と虚部を取り出して２次元プロット
# - 複素数の実部と虚部を取り出してそれぞれプロット
# - 複素数の絶対値と位相を取り出してそれぞれプロット

import numpy as np
import matplotlib.pyplot as plt

OUT_WAVE_FILE = "out_wave_beat.wav"

n_framerate = 16000             # 標本化周波数 (Hz)

FREQ = 2                        # 正弦波の周波数 (Hz)
DURATION = 1                    # 音の継続時間 (sec)
AMPLITUDE = 2.0                 # 正弦波の振幅

T = 1.0 / n_framerate           # 標本化周期 (sec)

# 複素正弦波の実部と虚部を作成
time = np.arange(0, DURATION, T)  # 継続時間に等しい標本点の作成
cos_wave = AMPLITUDE * np.cos(2 * np.pi * FREQ * time)  # 実部
sine_wave = AMPLITUDE * np.sin(2 * np.pi * FREQ * time)  # 虚部

# 複素正弦波作成: 虚数単位は 1j で作られる！
complex_sine_wave = cos_wave + 1j * sine_wave

# 実部と虚部を取り出して 2次元プロット
plt.figure(figsize=(6, 6))  # figureの縦横の大きさ
plt.scatter(complex_sine_wave.real, complex_sine_wave.imag)
plt.xlabel('Real part')
plt.xlabel('Imaginary part')
plt.show()

# 実部と虚部を取り出して それぞれプロット
plt.figure(figsize=(10, 7))
plt.subplot(2, 1, 1)
plt.plot(time, complex_sine_wave.real)
plt.xlabel("Time (sec)")
plt.ylabel("Real part")
plt.subplot(2, 1, 2)
plt.plot(time, complex_sine_wave.imag)
plt.xlabel("Time (sec)")
plt.ylabel("Imaginary part")
plt.show()

# 絶対値と位相を計算して それぞれプロット
amplitude = np.abs(complex_sine_wave)
phase = np.angle(complex_sine_wave)
plt.figure(figsize=(10, 7))
plt.subplot(2, 1, 1)
plt.plot(time, amplitude)
plt.xlabel("Time (sec)")
plt.ylabel("Absolute value")
plt.subplot(2, 1, 2)
plt.plot(time, phase)
plt.xlabel("Time (sec)")
plt.ylabel("Phase")
plt.show()
