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
# - リバーブをかける

import sox
from scipy.io import wavfile

IN_WAVE_FILE = "in.wav"  # 入力音声
OUT_WAVE_FILE = "reverb.wav"  # リバーブ済み音声

# create trasnformer (単一ファイルに対する処理)
transformer = sox.Transformer()

# #################### リバーブ の パラメタ ####################
# リバーブの残響音の長さを調整 (0-100 %)
REVERBERANCE = 80

# 高周波反響音の減衰率 (0-100 %)  0だと反響が長い、100だと反響が短い
# →高周波成分が残響の間でどれだけ「吸収」されるかをシミュレート
HIGH_FREQ_DAMPING = 30

# 反響する部屋の大きさ (0-100 %)  大きいとホール、小さいと風呂場とか
ROOM_SCALE = 20

STEREO_DEPTH = 100

# 反響が始まるまでの時間 (up to 500 ms) 大きいと遅れて残響→壁の反射を表現
PRE_DELAY = 100

# ウェットゲイン (dB)  付け加えた反響音そのものの大きさ
WET_GAIN = 0

# Trueはウェット成分のみ出力
WET_ONLY = False

# ##############################################################

# リバーブをかける
transformer.reverb(
    reverberance=REVERBERANCE,
    high_freq_damping=HIGH_FREQ_DAMPING,
    room_scale=ROOM_SCALE,
    stereo_depth=STEREO_DEPTH,
    pre_delay=PRE_DELAY,
    wet_gain=WET_GAIN,
    wet_only=WET_ONLY,
)
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE)

# リバーブをかけた結果をarrayとして取得
reverb = transformer.build_array(IN_WAVE_FILE)
