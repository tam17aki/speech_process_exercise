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
# - ホワイトノイズを生成し、正弦波に重畳
# - 重畳後の正弦波を音声としてwavに保存

import numpy as np
from scipy.io import wavfile

OUT_WAVE_FILE = "out_wave_noised.wav"

n_framerate = 16000             # 標本化周波数 (Hz)

freq = 1000                    # 正弦波の周波数 (Hz)
duration = 1                   # 音の継続時間 (sec)
amplitude = 8000               # 正弦波の振幅

noise_gain = 2000              # 雑音のゲイン

T = 1.0 / n_framerate          # 標本化周期 (sec)

# 正弦波作成
time = np.arange(0, duration, T)  # 継続時間に等しい標本点の作成
sine_wave = amplitude * np.sin(2 * np.pi * freq * time)

# ホワイトノイズ作成
noise = np.random.randn(len(time))

# ノイズのゲイン調整
noise *= noise_gain

# ノイズの重畳
sine_wave_noised = sine_wave + noise

# wavの書き込み (scipyモジュール) -> お手軽！
sine_wave = sine_wave.astype(np.int16)  # 16bit整数に変換
wavfile.write(OUT_WAVE_FILE, n_framerate, sine_wave_noised)
