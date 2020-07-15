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
# - 周波数の近い２つの正弦波を重ね合わせて「うなり」を発生させる
# - ヒルベルト変換による包絡線および瞬時位相の抽出
# - 包絡線と瞬時位相から波形の再構成

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

n_framerate = 16000             # 標本化周波数 (Hz)

freq1 = 6                       # 正弦波の周波数 (Hz)
freq2 = 4                       # 正弦波の周波数 (Hz)
duration = 2                    # 音の継続時間 (sec)
amplitude = 1.0                 # 正弦波の振幅

T = 1.0 / n_framerate           # 標本化周期 (sec)

# 正弦波作成
time = np.arange(0, duration, T)  # 継続時間に等しい標本点の作成
sine_wave1 = amplitude * np.sin(2 * np.pi * freq1 * time)
sine_wave2 = amplitude * np.sin(2 * np.pi * freq2 * time)

# うなり発生
sine_wave = sine_wave1 + sine_wave2

# ヒルベルト変換 (FFT -> 虚部0 & 実部2倍 -> 逆FFT)
envelop = np.abs(signal.hilbert(sine_wave))  # 包絡
angle = np.unwrap(np.angle(signal.hilbert(sine_wave)))  # 瞬時位相

# 波形と包絡線のプロット
fig = plt.figure(figsize=(10, 6))
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Original waveform & envelop")
plt.plot(time, sine_wave, label="original")
plt.plot(time, envelop, label="upper envelop")         # 上側の包絡
plt.plot(time[::-1], -envelop, label="lower envelop")  # 下側の包絡
plt.ylim(-3.2, 3.2)
plt.legend()
plt.show()

# 瞬時位相のプロット
fig = plt.figure(figsize=(10, 6))
plt.xlabel("Time [s]")
plt.ylabel("Phase [rad]")
plt.title("Instantatenous phase")
plt.plot(time, angle)
plt.show()

# オリジナルの波形と再構成後の波形
reconst = envelop * np.cos(angle)  # 再構成
fig = plt.figure(figsize=(10, 6))
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Original & reconstructed waveform")
plt.plot(time, sine_wave, label="original", linewidth=3)
plt.plot(time, reconst, label="reconstructed")
plt.ylim(-3.2, 3.2)
plt.legend()
plt.show()
