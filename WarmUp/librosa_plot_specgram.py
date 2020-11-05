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
# librosa を用いた波形プロット (やや処理が重たい)

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

# 短時間フーリエ変換
data_stft = librosa.stft(data, hop_length=HOP_LENGTH, n_fft=FRAME_LENGTH)

# 振幅スペクトル
data_ampspec = np.abs(data_stft)

# 振幅スペクトルをデシベルスケールにする
data_ampspec_dB = librosa.amplitude_to_db(data_ampspec, ref=np.max)

# プロット枠を確保 (10がヨコのサイズ、4はタテのサイズ)
plt.figure(figsize=(10, 4))

# スペクトログラムの表示
librosa.display.specshow(
    data_ampspec_dB, x_axis="time", y_axis="linear", hop_length=HOP_LENGTH, sr=fs
)

# x軸のラベル
plt.xlabel("Time (sec)")

# y軸のラベル
plt.ylabel("Hz")

# 画像のタイトル
plt.title("Spectrogram")

# 余白を少なくする
plt.tight_layout()

# 画像を画面表示 (必須)
plt.show()
