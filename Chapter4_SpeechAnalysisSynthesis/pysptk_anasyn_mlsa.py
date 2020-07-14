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
# - PySPTKによる音声の分析再合成 (MLSAフィルタ)

from pysptk.synthesis import MLSADF, Synthesizer
from scipy.io import wavfile
import librosa
import numpy as np
import pysptk

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

# 音声の切り出しと窓掛け
frames = librosa.util.frame(x, frame_length=FRAME_LENGTH,
                            hop_length=HOP_LENGTH).astype(np.float64).T
frames *= pysptk.blackman(FRAME_LENGTH)  # 窓掛け（ブラックマン窓）

# ピッチ抽出
pitch = pysptk.swipe(x, fs=fs, hopsize=HOP_LENGTH,
                     min=MIN_F0, max=MAX_F0, otype="pitch")

# 励振源信号(声帯音源)の生成
source_excitation = pysptk.excite(pitch, HOP_LENGTH)

# メルケプストラム分析（＝スペクトル包絡の抽出）
mc = pysptk.mcep(frames, ORDER, ALPHA)  # メルケプストラム係数の抽出

# メルケプストラム係数からMLSAディジタルフィルタ係数に変換
mlsa_coef = pysptk.mc2b(mc, ALPHA)

# MLSAフィルタの作成
synthesizer = Synthesizer(MLSADF(order=ORDER, alpha=ALPHA), HOP_LENGTH)

# 励振源信号でフィルタを駆動して音声を合成
y = synthesizer.synthesis(source_excitation, mlsa_coef)

# 音声の書き込み
y = y.astype(np.int16)
wavfile.write(OUT_WAVE_FILE, fs, y)
