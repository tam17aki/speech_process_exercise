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
# - ピッチシフトをかける（再生時間を変えずにピッチを上下させる）

import sox

IN_WAVE_FILE = "in.wav"         # 入力音声
OUT_WAVE_FILE_HIGH = "pitch_high.wav"  # ピッチシフト済み音声（音が高い）
OUT_WAVE_FILE_LOW = "pitch_low.wav"    # ピッチシフト済み音声（音が低い）

# create trasnformer (単一ファイルに対する処理)
transformer = sox.Transformer()

# ピッチシフト の パラメタ
# 単位：セミトーン（いわゆる半音 -> 1半音の変化は周波数的には約1.06倍）
# 正値は上げる、負値は下げる
# 実際にはfloat値を指定可能
PITCHSHIFT_HIGH = 3.0  # 3半音上げる
PITCHSHIFT_LOW = -5.0  # 5半音下げる

# ピッチシフトをかける
transformer.pitch(n_semitones=PITCHSHIFT_HIGH)  # 上げる
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE_HIGH)

transformer.pitch(n_semitones=PITCHSHIFT_LOW)   # 下げる
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE_LOW)
