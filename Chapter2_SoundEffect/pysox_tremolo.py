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
