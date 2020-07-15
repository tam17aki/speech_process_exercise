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
