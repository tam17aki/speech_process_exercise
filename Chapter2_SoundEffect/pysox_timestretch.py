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
# - タイムストレッチをかける（ピッチを変えずにテンポを変える）

import sox

IN_WAVE_FILE = "in.wav"       # 入力音声
OUT_WAVE_FILE = "tempo.wav"  # タイムストレッチ済み音声

# create trasnformer (単一ファイルに対する処理)
transformer = sox.Transformer()

# タイムストレッチ の パラメタ
FACTOR = 1.2  # 早くする (1.0より大きい) / 遅くする (1.0より小さい) 倍率

# タイムストレッチをかける
transformer.tempo(factor=FACTOR)
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE)
