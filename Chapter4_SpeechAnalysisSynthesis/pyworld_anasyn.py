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

from scipy.io import wavfile
import numpy as np
import pyworld

IN_WAVE_FILE = "in.wav"       # 入力音声
OUT_WAVE_FILE = "out.wav"     # 分析再合成した音声

# 音声の読み込み
fs, x = wavfile.read(IN_WAVE_FILE)
x = x.astype(np.float64)

# 音声の分析 (基本周波数、スペクトル包絡、非周期性指標)
f0, sp, ap = pyworld.wav2world(x, fs)

# 音声の再合成
y = pyworld.synthesize(f0, sp, ap, fs)
y = y.astype(np.int16)

# wavファイルに保存
wavfile.write(OUT_WAVE_FILE, fs, y)
