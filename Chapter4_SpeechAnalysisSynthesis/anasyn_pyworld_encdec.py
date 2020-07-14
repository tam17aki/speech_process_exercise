#!/usr/bin/env python3

""" 音声情報処理 n本ノック !! """

# Copyright (C) 2020 by Akira TAMAMORI

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Commentary:
# - PyWORLDによる音声の分析再合成
# - ただしスペクトル包絡と非周期性指標をエンコード/デコード

import pyworld as pw
from scipy.io import wavfile
import numpy as np

IN_WAVE_FILE = "in.wav"       # 入力音声
OUT_WAVE_FILE = "out.wav"     # 分析再合成した音声

SP_DIM = 50                     # スペクトル包絡の圧縮後の次元

# 音声の読み込み
fs, x = wavfile.read(IN_WAVE_FILE)
x = x.astype(np.float64)

# 音声の分析 (基本周波数、スペクトル包絡、非周期性指標)
f0, sp, ap = pw.wav2world(x, fs)
fft_size = pw.get_cheaptrick_fft_size(fs)

# スペクトル包絡をエンコード / デコード
# https://www.isca-speech.org/archive/Interspeech_2017/abstracts/0067.html
code_sp = pw.code_spectral_envelope(sp, fs, SP_DIM)
decode_sp = pw.decode_spectral_envelope(code_sp, fs, fft_size)

# 非周期性指標をエンコード / デコード
code_ap = pw.code_aperiodicity(ap, fs)
decode_ap = pw.decode_aperiodicity(code_ap, fs, fft_size)

# 音声の再合成
y = pw.synthesize(f0, decode_sp, decode_ap, fs)
y = y.astype(np.int16)

# 音声の書き込み
wavfile.write(OUT_WAVE_FILE, fs, y)
