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
# - 音声からケプストラム法により基本周波数を推定する
# - パワーが最大となる音声フレームを対象に推定

import numpy as np
import scipy
from scipy.io import wavfile
import librosa
import matplotlib.pyplot as plt

IN_WAVE_FILE = "in.wav"         # 分析対象の音声

FRAME_LENGTH = 1024             # フレーム長 (FFTサイズ)
HOP_LENGTH = 80                 # フレームのシフト長
FFT_LENGTH = FRAME_LENGTH

MAX_Fo = 400                    # 分析における基本周波数の最大値 (Hz)
MIN_Fo = 80                     # 分析における基本周波数の最小値 (Hz)

# 音声のロード
fs, data = wavfile.read(IN_WAVE_FILE)
data = data.astype(np.float64)

# ケプストラムの最大次数、最小次数
max_cep_order = int(np.floor(fs / MIN_Fo))
min_cep_order = int(np.floor(fs / MAX_Fo))

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

# ケプストラムの計算 (FFT → 絶対値 → 対数 → 逆FFT)
fft_spec = scipy.fft.rfft(windowed_frame)
log_amp_spec = np.log(np.abs(fft_spec))
cepstrum = scipy.fft.irfft(log_amp_spec)

# ピーク位置の検出
peak_index = np.argmax(cepstrum[min_cep_order: max_cep_order])
max_quef = peak_index + min_cep_order

# ケフレンシに変換して基本周波数の推定
fo = fs / max_quef
print(f"Fundamental Frequency = {fo:.2f} Hz")

# 波形表示
fig = plt.figure(figsize=(12, 8))
time = np.arange(len(windowed_frame)) / fs
axes = fig.add_subplot(3, 1, 1)
axes.plot(time, pow_max_frame, label="original")
axes.plot(time, windowed_frame, label="windowed")
axes.set_xlabel("Time (sec)")
axes.set_ylabel("Amplitude")
axes.set_title("Waveform")
axes.legend()
axes.set_xlim(0, np.max(time))

# 相対パワー表示
axes = fig.add_subplot(3, 1, 2)
freq = fs/2 * np.arange(len(log_amp_spec)) / len(log_amp_spec)
logpower = 20 * np.log(np.abs(fft_spec) / np.max(np.abs(fft_spec)))
axes.plot(freq, logpower, label="original")
axes.set_xlabel("Frequency (Hz)")
axes.set_ylabel("Log power (dB)")
axes.set_title("Log spectrum")
axes.set_xlim(0, np.max(freq))
axes.set_ylim(np.min(logpower), 0)

# ケプストラム表示 (対数振幅)
axes = fig.add_subplot(3, 1, 3)
quef = np.arange(FFT_LENGTH / 2) / fs
log_cepstrum = np.log(np.abs(cepstrum))
axes.plot(quef, log_cepstrum[:len(quef)])
axes.set_xlabel("Quefrency (sec)")
axes.set_ylabel("Log amplitude (dB)")
axes.set_title("Cepstrum")
axes.set_xlim(0, np.max(quef))

plt.tight_layout()
plt.show()
