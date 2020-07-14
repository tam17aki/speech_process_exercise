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
# - リバーブをかける

import sox

IN_WAVE_FILE = "in.wav"       # 入力音声
OUT_WAVE_FILE = "reverb.wav"    # リバーブ済み音声

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
transformer.reverb(reverberance=REVERBERANCE,
                   high_freq_damping=HIGH_FREQ_DAMPING,
                   room_scale=ROOM_SCALE,
                   stereo_depth=STEREO_DEPTH,
                   pre_delay=PRE_DELAY,
                   wet_gain=WET_GAIN,
                   wet_only=WET_ONLY)
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE)
