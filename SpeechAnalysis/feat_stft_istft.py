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
# 短時間フーリエ変換と逆変換
# 波形読み込みはscipy.ioのwavfileモジュール

import numpy as np
import scipy.signal as sp
from scipy.io import wavfile

IN_WAVE_FILE = "in.wav"  # モノラル音声（前提）
OUT_WAVE_FILE = "out_istft.wav"

FRAME_LENGTH = 512  # フレーム長
HOP_LENGTH = 256  # フレームのシフト長
N_OVERLAP = FRAME_LENGTH - HOP_LENGTH  # オーバーラップ幅

# 音声データ読み込み (fsがサンプリング周波数、dataは音声データ)
fs, data = wavfile.read(IN_WAVE_FILE)

# 短時間フーリエ変換によりフーリエスペクトル系列を得る
_, _, stft_data = sp.stft(
    data, fs=fs, window="hann", nperseg=FRAME_LENGTH, noverlap=N_OVERLAP
)

# 短時間フーリエ逆変換により音声に戻す
_, data_inv = sp.istft(
    stft_data, fs=fs, window="hann", nperseg=FRAME_LENGTH, noverlap=N_OVERLAP
)

# 音声の書き込み
data_inv = data_inv.astype(np.int16)  # 2byte (16 bit)の整数値に変換
wavfile.write(OUT_WAVE_FILE, fs, data_inv)
