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
# - PySPTKによる音声の分析再合成 (MLSAフィルタ)
# - ただしメルケプストラム係数をWORLDから抽出したスペクトル包絡から計算

from pysptk.synthesis import MLSADF, Synthesizer
from scipy.io import wavfile
import numpy as np
import pysptk
import pyworld

FRAME_LENGTH = 1024
HOP_LENGTH = 80
MIN_F0 = 60
MAX_F0 = 240
ORDER = 25
ALPHA = 0.41

IN_WAVE_FILE = "in.wav"       # 入力音声
OUT_WAVE_FILE = "out.wav"     # 分析再合成した音声

# 音声の読み込み
fs, x = wavfile.read(IN_WAVE_FILE)
x = x.astype(np.float64)

# 音声の分析 (基本周波数、スペクトル包絡、非周期性指標)
_, sp, _ = pyworld.wav2world(x, fs)

# メルケプストラム係数の抽出 from WORLDのスペクトル包絡
mcep = pysptk.sp2mc(sp, order=ORDER, alpha=ALPHA)

# ピッチ抽出
pitch = pysptk.swipe(x, fs=fs, hopsize=HOP_LENGTH,
                     min=MIN_F0, max=MAX_F0, otype="pitch")

# 励振源信号(声帯音源)の生成
source_excitation = pysptk.excite(pitch, HOP_LENGTH)

# メルケプストラム係数からMLSAディジタルフィルタ係数に変換
mlsa_coef = pysptk.mc2b(mcep, ALPHA)

# MLSAフィルタの作成
synthesizer = Synthesizer(MLSADF(order=ORDER, alpha=ALPHA), HOP_LENGTH)

# 励振源信号でMLSAフィルタを駆動して音声を合成
y = synthesizer.synthesis(source_excitation, mlsa_coef)

# 音声の書き込み
y = y.astype(np.int16)
wavfile.write(OUT_WAVE_FILE, fs, y)
