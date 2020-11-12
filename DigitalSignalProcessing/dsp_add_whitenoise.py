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
# - 音声に白色雑音を混ぜる
# - scipyを用いたwav出力
# - matplotlibによるプロット（元音声と雑音入り音声）

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

IN_WAVE_FILE = "in.wav"  # モノラル音声（前提）
OUT_WAVE_FILE = "out_whitenoise.wav"

# 音声データ読み込み (fsがサンプリング周波数、dataは音声データ)
fs, speech_data = wavfile.read(IN_WAVE_FILE)

# 音声データの長さ
n_speech = len(speech_data)

# 雑音だけの区間の長さ
n_noise = 4000

# 全体の長さ
n_samples = n_noise + n_speech

# 白色雑音を生成
white_noise = np.random.normal(scale=0.04, size=n_samples)

# 2バイトのデータとして書き込むためにスケールを調整
white_noise = white_noise * np.iinfo(np.int16).max

# ゲインを調整
white_noise = 0.5 * white_noise

# 白色雑音を混ぜる
mixed_signal = white_noise  # 最初に雑音を入れる
mixed_signal[n_noise:] += speech_data  # 後から音声を足す

# wavの書き込み (scipyモジュール)
mixed_signal = mixed_signal.astype(np.int16)  # 16bit整数に変換
wavfile.write(OUT_WAVE_FILE, fs, mixed_signal)

# プロット枠を確保 (10がヨコのサイズ、4はタテのサイズ)
fig = plt.figure(figsize=(12, 8))
axes1 = fig.add_subplot(2, 1, 1)
n_samples = len(speech_data)
time = np.arange(n_samples) / fs
axes1.plot(time, speech_data)  # 音声データのプロット
axes1.set_xlabel("Time (sec)")  # x軸のラベル
axes1.set_ylabel("Amplitude")  # y軸のラベル
axes1.set_title("Original speech")

axes2 = fig.add_subplot(2, 1, 2)
n_samples = len(mixed_signal)
time = np.arange(n_samples) / fs
axes2.plot(time, mixed_signal)  # 音声データのプロット
axes2.set_xlabel("Time (sec)")  # x軸のラベル
axes2.set_ylabel("Amplitude")  # y軸のラベル
axes2.set_title("Mixed speech (original + white noise)")

# 画像を画面表示
plt.tight_layout()
plt.show()
