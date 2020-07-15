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
# - 正弦波の周波数を指定して「聞くことのできる」波を作る
# - 周波数の近い２つの正弦波を重ね合わせて「うなり」を発生させる
# - scipyを用いたwav出力

import numpy as np
from scipy.io import wavfile

OUT_WAVE_FILE = "out_wave_beat.wav"

n_framerate = 16000             # 標本化周波数 (Hz)

freq1 = 500                     # 正弦波の周波数 (Hz)
freq2 = 504                     # 正弦波の周波数 (Hz)
duration = 2                    # 音の継続時間 (sec)
amplitude = 8000                # 正弦波の振幅

T = 1.0 / n_framerate           # 標本化周期 (sec)

# 正弦波作成
time = np.arange(0, duration, T)  # 継続時間に等しい標本点の作成
sine_wave1 = amplitude * np.sin(2 * np.pi * freq1 * time)
sine_wave2 = amplitude * np.sin(2 * np.pi * freq2 * time)

# うなり発生
sine_wave = sine_wave1 + sine_wave2

# wavの書き込み (scipyモジュール)
sine_wave = sine_wave.astype(np.int16)  # 16bit整数に変換
wavfile.write(OUT_WAVE_FILE, n_framerate, sine_wave)
