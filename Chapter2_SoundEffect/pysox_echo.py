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
# - エコーをかける

import sox

IN_WAVE_FILE = "in.wav"       # 入力音声
OUT_WAVE_FILE = "echo.wav"    # エコー済み音声

# create trasnformer (単一ファイルに対する処理)
transformer = sox.Transformer()

# エコー の パラメタ
n_echos = 2     # エコー回数
delays = [375]  # 遅延時間 (ms)
decays = [0.5]  # 減衰率

# エコー回数分、遅延時間と減衰率を与える必要がある
# → エコー回数に等しい長さの「リスト」を 遅延時間と減衰率それぞれで用意する
# → n_echos が 2 なら遅延時間は [375, 750], 減衰率は [0.5, 0.25]
for i in range(1, n_echos):
    delays.append(delays[0] * (i + 1))   # 遅延時間は線形的
    decays.append(decays[0] ** (i + 1))  # 減衰率は指数的

# エコーをかける
transformer.echo(n_echos=n_echos, delays=delays, decays=decays)
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE)
