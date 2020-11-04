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
# matplotlib を用いた波形プロット
# 波形読み込みはwaveモジュール

import wave

import matplotlib.pyplot as plt
import numpy as np

IN_WAVE_FILE = "mono.wav"  # モノラル音声（前提）

# wavの読み込み
with wave.open(IN_WAVE_FILE, "r") as sound:
    params = sound.getparams()
    n_channel = sound.getnchannels()  # チャネル数 (mono:1, stereo:2)
    bitdepth = sound.getsampwidth()  # 量子化ビット数 (byte!)
    sample_freq = sound.getframerate()  # サンプリング周波数
    n_frames = sound.getnframes()  # チャネルあたりのサンプル数
    n_samples = n_channel * n_frames  # 総サンプル数
    data = sound.readframes(n_frames)  # 音声データ (bytesオブジェクト)


# 2バイト(16bit)の整数値系列に変換
data = np.frombuffer(data, dtype=np.int16)

# 時間軸を設定
n_samples = len(data)
time = np.arange(n_samples) / sample_freq

# 音声データのプロット
plt.plot(time, data)

# x軸のラベル
plt.xlabel("Time (sec)")

# y軸のラベル
plt.ylabel("Amplitude")

# 画像のタイトル
plt.title("Waveform")

# 画像を画面表示
plt.show()
