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
# - PySoXを用いた音声情報処理シリーズ
# - ローパスフィルタ/ハイパスフィルタをかける

import sox

IN_WAVE_FILE = "in.wav"       # 入力音声
OUT_WAVE_FILE_LOW = "lowpass.wav"    # ローパスフィルタ適用済み音声
OUT_WAVE_FILE_HIGH = "highpass.wav"  # ハイパスフィルタ適用済み音声

transformer = sox.Transformer()

# 遮断周波数は -3dB（パワーは0.501倍、振幅は0.708倍）になる周波数
LOWPASS_FREQ = 1000  # ローパスフィルタの遮断周波数 (Hz)
HIGHPASS_FREQ = 1000  # ハイパスフィルタの遮断周波数 (Hz)

# ローパスフィルタ
transformer.lowpass(frequency=LOWPASS_FREQ)
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE_LOW)

# ハイパスフィルタ
transformer.highpass(frequency=HIGHPASS_FREQ)
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE_HIGH)
