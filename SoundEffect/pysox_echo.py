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
# - エコーをかける


import sox
from scipy.io import wavfile

IN_WAVE_FILE = "in.wav"  # 入力音声
OUT_WAVE_FILE = "echo.wav"  # エコー済み音声

# トランスフォーマーをつくる（単一音声に対する処理）
transformer = sox.Transformer()

# エコー の パラメタ
n_echos = 2  # エコー回数
delays = [375]  # 遅延時間 (ms)
decays = [0.5]  # 減衰率

# エコー回数分、遅延時間と減衰率を与える必要がある
# → エコー回数に等しい長さの「リスト」を 遅延時間と減衰率それぞれで用意する
# → n_echos が 2 なら遅延時間は [375, 750], 減衰率は [0.5, 0.25]
for i in range(1, n_echos):
    delays.append(delays[0] * (i + 1))  # 遅延時間は線形的
    decays.append(decays[0] ** (i + 1))  # 減衰率は指数的

# transformerにエコーを設定する
transformer.echo(n_echos=n_echos, delays=delays, decays=decays)

# エコーをかけた結果をファイルに保存
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE)

# エコーをかけた結果をarrayとして取得
echos = transformer.build_array(IN_WAVE_FILE)
