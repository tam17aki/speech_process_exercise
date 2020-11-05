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
# - フランジャ（うなり、うねり）をかける

import sox

IN_WAVE_FILE = "in.wav"  # 入力音声
OUT_WAVE_FILE = "flanger.wav"  # フランジャをかけた音声

# create trasnformer (単一ファイルに対する処理)
transformer = sox.Transformer()

# フランジャ の パラメタ
DELAY = 15  # 大もとの遅延時間 (ms)
DEPTH = 3  # DELAY ± DEPTHの遅延をかける (ms)
REGEN = 0  # 出力をフィードバックするときのゲイン量 (-95 to 95)
WIDTH = 75  # ディレイさせた音の振幅をどれだけ減衰させたうえで重ねるか (%)
SPEED = 1.0  # うなりの速さ; 遅延時間の揺れの速さ (Hz)
SHAPE = "sine"  # フランジャのスイープ特性;
# sine的に遅延時間が変化 or 三角波("triangle")的に遅延時間が変化

PHASE = 0  # 多チャネルの音にフランジャをかけるときの位相ずれ率 (%)

# transformerにフランジャを設定する
transformer.flanger(
    delay=DELAY,
    depth=DEPTH,
    regen=REGEN,
    width=WIDTH,
    speed=SPEED,
    shape="sine",
    phase=PHASE,
)

# フランジャをかけた結果をファイルに保存
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE)

# フランジャをかけた結果をarrayとして取得
flangers = transformer.build_array(IN_WAVE_FILE)
