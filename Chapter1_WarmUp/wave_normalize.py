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
# 振幅を正規化

import wave
import numpy as np

IN_WAVE_FILE = "in.wav"   # 16bit モノラル音声（前提）
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

# 振幅の正規化
x = np.frombuffer(sound_frames, dtype=np.int16)
x = (x / np.max(x)) * (2 ** (bitdepth * 8 - 1) - 1)
x = x.astype(np.int16)
sound_frames = x.tobytes()

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
