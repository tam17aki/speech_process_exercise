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
# matplotlib を用いたスペクトログラムのプロット
# 波形読み込みはscipy.ioのwavfileモジュール

import matplotlib.pyplot as plt
from scipy.io import wavfile

IN_WAVE_FILE = "in.wav"  # モノラル音声（前提）

FRAME_LENGTH = 1024  # フレーム長
HOP_LENGTH = 80  # フレームのシフト長
FFT_LENGTH = FRAME_LENGTH  # FFTサイズ
N_OVERLAP = FRAME_LENGTH - HOP_LENGTH  # オーバーラップ幅

# 音声データ読み込み (fsがサンプリング周波数、dataは音声データ)
fs, data = wavfile.read(IN_WAVE_FILE)

# スペクトログラムのプロット
plt.specgram(data, NFFT=FFT_LENGTH, noverlap=N_OVERLAP, Fs=fs, cmap="jet")

# x軸のラベル
plt.xlabel("Time (sec)")

# y軸のラベル
plt.ylabel("Frequency (Hz)")

# 画像のタイトル
plt.title("Spectrogram")

# 画像を画面表示
plt.show()
