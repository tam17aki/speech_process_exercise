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
# 量子化ビット数を変更したwavファイルの作成

import wave
import numpy as np

IN_WAVE_FILE = "in.wav"  # 16bit モノラル音声（前提）
OUT_WAVE_FILE = "out.wav"

# wavの読み込み
with wave.open(IN_WAVE_FILE, "r") as sound:
    params = sound.getparams()
    n_channel = sound.getnchannels()    # チャネル数 (mono:1, stereo:2)
    bitdepth = sound.getsampwidth()     # 量子化ビット数 (byte!)
    n_framerate = sound.getframerate()  # サンプリング周波数
    n_frames = sound.getnframes()       # チャネルあたりのサンプル数
    n_samples = n_channel * n_frames    # 総サンプル数
    sound_frames = sound.readframes(n_frames)  # 音声データ (bytesオブジェクト)

# ヘッダ情報の表示
print(f"入力ファイル名: {IN_WAVE_FILE}")
print(f"  ・チャネル数: {n_channel}")
print(f"  ・量子化ビット数: {bitdepth * 8}")
print(f"  ・サンプリング周波数: {n_framerate}")
print(f"  ・サンプル数: {n_samples}")

# 量子化ビット数 変更 (16bit to 8bit) →下位ビットを捨てない
x = np.frombuffer(sound_frames, dtype=np.int16)
volume = np.max(x) / (2 ** 16)
x = (x / np.max(x)) * (2 ** 7 - 1)
x *= volume
x = x.astype(np.int8)
sound_frames = x.tobytes()

# ヘッダ情報の変更
bitdepth = 1  # 2 byte to 1byte

# wavの書き込み
with wave.open(OUT_WAVE_FILE, "w") as sound:
    sound.setnchannels(n_channel)    # チャネル数 (mono:1, stereo:2)
    sound.setsampwidth(bitdepth)     # 量子化ビット数 (byte!)
    sound.setframerate(n_framerate)  # 標本化周波数の変更
    sound.setnframes(n_frames)       # チャネルあたりのサンプル数
    sound.writeframes(sound_frames)  # 音声データの書き込み

print(f"出力ファイル名: {OUT_WAVE_FILE}")
print(f"  ・チャネル数: {n_channel}")
print(f"  ・量子化ビット数: {bitdepth * 8}")
print(f"  ・サンプリング周波数: {n_framerate}")
print(f"  ・サンプル数: {n_samples}")
