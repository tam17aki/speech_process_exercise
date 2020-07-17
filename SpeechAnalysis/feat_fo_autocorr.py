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
# - 自己相関法により基本周波数を推定する

import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.io import wavfile
import librosa

IN_WAVE_FILE = "in.wav"         # 分析対象の音声

FRAME_LENGTH = 1024             # フレーム長 (FFTサイズ)
HOP_LENGTH = 80                 # フレームのシフト長
FFT_LENGTH = FRAME_LENGTH

MAX_Fo = 200                # 分析における基本周波数の最大値 (Hz)
MIN_Fo = 60                 # 分析における基本周波数の最小値 (Hz)

# 音声のロード
fs, data = wavfile.read(IN_WAVE_FILE)
data = data.astype(np.float64)

# フレーム化
frames = librosa.util.frame(data, frame_length=FRAME_LENGTH,
                            hop_length=HOP_LENGTH).T

# パワーが最大のフレーム位置を取得
max_ind = np.argmax(np.sum(frames * frames, axis=1))

# パワーが最大となるフレームを取り出す
pow_max_frame = frames[max_ind, :]

# 窓掛け
window = scipy.signal.blackman(FFT_LENGTH)
windowed_frame = pow_max_frame * window

# 自己相関関数の計算
autocorr = scipy.signal.correlate(windowed_frame, windowed_frame)
autocorr /= np.max(autocorr)    # 正規化

# 「右半分」を取得
autocorr = autocorr[int(len(autocorr) / 2):]

# 自己相関関数の極大点を与えるインデックスを取得（ピーク位置）
relmax_index = scipy.signal.argrelmax(autocorr)[0]
relmin_index = scipy.signal.argrelmin(autocorr)[0]

# 各ピーク位置における自己相関関数の値のうち、
# 最大値を与えるときのピーク位置を計算
peak_index = np.argmax(autocorr[relmax_index])

# ピーク位置を基本周期に変換
period = relmax_index[peak_index] / fs

# 基本周波数を計算
fo = 1.0 / period
print(f"Fundamental Frequency = {fo:.2f} Hz")

# 波形を表示
fig = plt.figure(figsize=(12, 6))
time = np.arange(len(windowed_frame)) / fs
axes = fig.add_subplot(2, 1, 1)
axes.plot(time, pow_max_frame, label="original")
axes.plot(time, windowed_frame, label="windowed")
axes.set_xlabel("Time (sec)")
axes.set_ylabel("Amplitude")
axes.set_title("Waveform")
axes.legend()

# 自己相関関数と極大値を表示
axes = fig.add_subplot(2, 1, 2)
axes.plot(time, autocorr, label="autocorrelation")
axes.plot(time[relmax_index], autocorr[relmax_index], marker="o",
          linestyle='', label="local maximum")
axes.plot([0], autocorr[0], marker="o", linestyle='', color='#ff7f00')
axes.plot(time[relmax_index[peak_index]],
          autocorr[relmax_index[peak_index]],
          marker="o", markersize='10', linestyle='', color='blue',
          label="fundamental period")
axes.set_xlabel("Time (sec)")
axes.set_ylabel("Autocorrelation function")
axes.set_title("Fundamental frequency estimation "
               f"via autocorrelation method: fo = {fo:.2f} Hz")
plt.tight_layout()
plt.legend()

plt.show()
