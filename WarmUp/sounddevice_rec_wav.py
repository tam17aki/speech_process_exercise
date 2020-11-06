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
# sounddeviceモジュールによる録音
# 波形書き込みはwaveモジュール

import wave

import numpy as np
import sounddevice as sd

OUT_WAVE_FILE = "out.wav"

fs = 16000  # サンプリング周波数 (Hz)
duration = 3  # 録音時間 (sec)
n_channels = 1  # モノラル

n_frames = int(fs * duration)  # 総サンプル数

# 音声の録音
data = sd.rec(frames=n_frames, samplerate=fs, channels=n_channels)
sd.wait()

# 振幅の正規化
data = data / data.max() * np.iinfo(np.int16).max

# floatを2byte整数に変換
data = data.astype(np.int16)

# wavの書き込み
with wave.open(OUT_WAVE_FILE, mode="wb") as sound:
    sound.setnchannels(n_channels)  # モノラル
    sound.setsampwidth(2)  # 量子化ビット数 (byte表示)
    sound.setframerate(fs)
    sound.writeframes(data.tobytes())
