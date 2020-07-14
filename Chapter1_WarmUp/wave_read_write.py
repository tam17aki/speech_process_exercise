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
# waveモジュールを用いた音声入出力 (コピー作成)

import wave

IN_WAVE_FILE = "in.wav"  # モノラル音声（前提）
OUT_WAVE_FILE = "out.wav"

# wavの読み込み
with wave.open(IN_WAVE_FILE, "r") as sound:
    params = sound.getparams()
    n_channel = sound.getnchannels()    # チャネル数 (mono:1, stereo:2)
    bitdepth = sound.getsampwidth()     # 量子化ビット数 (byte!)
    sample_freq = sound.getframerate()  # サンプリング周波数
    n_frames = sound.getnframes()       # チャネルあたりのサンプル数
    n_samples = n_channel * n_frames    # 総サンプル数
    sound_frames = sound.readframes(n_frames)  # 音声データ (bytesオブジェクト)

# ヘッダ情報の表示
print(f"チャネル数: {n_channel}")
print(f"量子化ビット数: {bitdepth * 8}")
print(f"サンプリング周波数: {sample_freq}")
print(f"サンプル数: {n_samples}")

# wavの書き込み
with wave.open(OUT_WAVE_FILE, "w") as sound:
    sound.setparams(params)   # ヘッダ情報の書き込み
    sound.writeframes(sound_frames)  # 音声データの書き込み
