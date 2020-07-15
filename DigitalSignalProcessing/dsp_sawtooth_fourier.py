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
# - ノコギリ波をフーリエ級数近似により作成する
# - scipyを用いたwav出力

import numpy as np
import numpy.matlib
from scipy.io import wavfile

OUT_WAVE_FILE = "out_sawtooh.wav"

sample_rate = 16000             # 標本化周波数 (Hz)
freq = 500                      # ノコギリ波の周波数 (Hz)
duration = 1                    # ノコギリ波の継続時間 (sec)
amplitude = 8000                # 振幅 (ゲイン)
order = 1000                    # 級数近似における倍音次数の上限値

period = 1.0 / freq             # ノコギリ波の周期 (sec)

# 標本点の数
sample_num = int(np.floor(duration * sample_rate))

# 標本点
time_axis = np.arange(0, sample_num).T / sample_rate

# フーリエ級数の倍音の次数 (1倍音, 2倍音, 3倍音,...)
orders = np.arange(1, order)  # 引数 start, stop, step

# ノコギリ波のフーリエ係数
coef = -1.0 * duration / (np.pi * orders) * np.cos(np.pi * orders)

# ノコギリ波の級数近似
sawtooth_wav = np.empty(sample_num)
for n, t in enumerate(time_axis):
    sawtooth_wav[n] = coef.dot(np.sin(2 * np.pi * orders * t / period))

sawtooth_wav *= amplitude

# wavの書き込み
sawtooth_wav = sawtooth_wav.astype(np.int16)  # 16bit整数に変換
wavfile.write(OUT_WAVE_FILE, sample_rate, sawtooth_wav)
