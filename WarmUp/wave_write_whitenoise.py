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
# 白色雑音をwavとして書き込む

import wave

import numpy as np

OUT_WAVE_FILE = "out_whitenoise.wav"

# 白色雑音のサンプル数を設定
n_samples = 40000

# サンプリング周波数
sample_freq = 16000

# 白色雑音を生成
data = np.random.normal(scale=0.1, size=n_samples)

# 値の範囲を調整
data = data * np.iinfo(np.int16).max

# 2バイト(16bit)の整数値に変換
data = data.astype(np.int16)

# wavの書き込み
with wave.open(OUT_WAVE_FILE, "w") as sound:
    sound.setnchannels(1)  # モノラル
    sound.setsampwidth(2)  # 量子化ビット数（2byte = 16bit）
    sound.setframerate(sample_freq)  # サンプリング周波数
    sound.writeframes(data)  # 音声データの書き込み
