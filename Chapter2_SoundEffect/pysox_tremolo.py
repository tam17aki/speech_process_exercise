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
# - トレモロをかける （周期的な振幅の上下動）

import sox

IN_WAVE_FILE = "in.wav"       # 入力音声
OUT_WAVE_FILE = "tremolo.wav"  # トレモロ済み音声

# create trasnformer (単一ファイルに対する処理)
transformer = sox.Transformer()

# トレモロ の パラメタ
# トレモロの速度 (Hz) → 振幅の上下動の頻度
SPEED = 10

# トレモロの深さ (%) → 振幅の上下動の深さ（当該振幅を基準にした比）
DEPTH = 50

# トレモロをかける
transformer.tremolo(speed=SPEED, depth=DEPTH)
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE)
