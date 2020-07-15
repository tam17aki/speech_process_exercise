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
# - PyWORLDによる音声の分析再合成
# - ただしスペクトル包絡と非周期性指標をエンコード/デコード

from scipy.io import wavfile
import numpy as np
import pyworld

IN_WAVE_FILE = "in.wav"       # 入力音声
OUT_WAVE_FILE = "out.wav"     # 分析再合成した音声

SP_DIM = 50                     # スペクトル包絡の圧縮後の次元

# 音声の読み込み
fs, x = wavfile.read(IN_WAVE_FILE)
x = x.astype(np.float64)

# 音声の分析 (基本周波数、スペクトル包絡、非周期性指標)
f0, sp, ap = pyworld.wav2world(x, fs)
fft_size = pyworld.get_cheaptrick_fft_size(fs)

# スペクトル包絡をエンコード / デコード
# https://www.isca-speech.org/archive/Interspeech_2017/abstracts/0067.html
code_sp = pyworld.code_spectral_envelope(sp, fs, SP_DIM)
decode_sp = pyworld.decode_spectral_envelope(code_sp, fs, fft_size)

# 非周期性指標をエンコード / デコード
code_ap = pyworld.code_aperiodicity(ap, fs)
decode_ap = pyworld.decode_aperiodicity(code_ap, fs, fft_size)

# 音声の再合成
y = pyworld.synthesize(f0, decode_sp, decode_ap, fs)
y = y.astype(np.int16)

# 音声の書き込み
wavfile.write(OUT_WAVE_FILE, fs, y)
