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
# scipyによるstft計算とlibrosaを用いた表示

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

IN_WAVE_FILE = "in.wav"  # モノラル音声（前提）

FRAME_LENGTH = 1024  # フレーム長
HOP_LENGTH = 80  # フレームのシフト長

# 音声データ読み込み (fsがサンプリング周波数、dataは音声データ)
fs, data = wavfile.read(IN_WAVE_FILE)
data = data.astype(np.float64)

# 短時間フーリエ変換（結果は複素数の系列）
data_stft = librosa.stft(data, hop_length=HOP_LENGTH, n_fft=FRAME_LENGTH)

# 振幅スペクトル（絶対値）
data_ampspec = np.abs(data_stft)

# 振幅スペクトルをデシベルスケールにする
data_ampspec_dB = librosa.amplitude_to_db(data_ampspec, ref=np.max)

# 振幅スペクトル系列の表示 (y軸はlinearスケール(Hz))
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
librosa.display.specshow(
    data_ampspec,
    x_axis="time",
    y_axis="linear",
    hop_length=HOP_LENGTH,
    sr=fs,
    ax=axes[0],
)
axes[0].set_xlabel("Time (sec)")
axes[0].set_ylabel("Hz")
axes[0].set_title("Amplitude Spectrogram (linear scale)")
librosa.display.specshow(
    data_ampspec_dB,
    x_axis="time",
    y_axis="linear",
    hop_length=HOP_LENGTH,
    sr=fs,
    ax=axes[1],
)
axes[1].set_xlabel("Time (sec)")
axes[1].set_ylabel("Hz")
axes[1].set_title("Amplitude Spectrogram (dB scale)")
plt.tight_layout()
plt.show()

# 振幅スペクトル系列の表示 (y軸が対数スケール)
# matplotlib由来の警告が出ますが気にしない (librosa側が未対応)
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
librosa.display.specshow(
    data_ampspec,
    x_axis="time",
    y_axis="log",
    hop_length=HOP_LENGTH,
    sr=fs,
    ax=axes[0],
)
axes[0].set_xlabel("Time (sec)")
axes[0].set_ylabel("Hz")
axes[0].set_title("Amplitude Spectrogram (linear scale)")
librosa.display.specshow(
    data_ampspec_dB,
    x_axis="time",
    y_axis="log",
    hop_length=HOP_LENGTH,
    sr=fs,
    ax=axes[1],
)
axes[1].set_xlabel("Time (sec)")
axes[1].set_ylabel("Hz")
axes[1].set_title("Amplitude Spectrogram (dB scale)")
plt.tight_layout()
plt.show()

# 位相スペクトルの計算
data_phasespec = np.angle(data_stft)

# 位相スペクトル系列の表示
plt.figure(figsize=(10, 4))
librosa.display.specshow(
    data_phasespec, x_axis="time", y_axis="linear", hop_length=HOP_LENGTH, sr=fs
)
plt.xlabel("Time (sec)")
plt.ylabel("Hz")
plt.title("Phase Spectrogram")
plt.tight_layout()
plt.show()
