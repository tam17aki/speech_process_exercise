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
# - ディジタルな正弦波を作成する
# - 正弦波の周波数を指定して「聞くことのできる」波を作る
# - waveモジュールを用いたwav出力
# - scipyを用いたwav出力

import wave
import numpy as np
from scipy.io import wavfile

OUT_WAVE_FILE = "out_wave.wav"
OUT_SCIPY_WAVE_FILE = "out_scipy.wav"

n_channel = 1                   # モノラル
bitdepth = 2                    # 量子化ビット数 16 bit (2 byte)
n_framerate = 16000             # 標本化周波数 (Hz)

freq = 1000                     # 正弦波の周波数 (Hz)
duration = 2                    # 音の継続時間 (sec)
amplitude = 8000                # 正弦波の振幅

T = 1.0 / n_framerate           # 標本化周期 (sec)

# 正弦波作成
time = np.arange(0, duration, T)  # 継続時間に等しい標本点の作成
sine_wave = amplitude * np.sin(2 * np.pi * freq * time)

# サンプル数
n_frames = len(sine_wave)

# bytesオブジェクトへの変換
sound_frames = sine_wave.astype(np.int16).tobytes()

# wavの書き込み (waveモジュール)
with wave.open(OUT_WAVE_FILE, "w") as sound:
    sound.setnchannels(n_channel)    # チャネル数
    sound.setsampwidth(bitdepth)     # 量子化ビット数 (byte!)
    sound.setframerate(n_framerate)  # 標本化周波数 (Hz)
    sound.setnframes(n_frames)       # チャネルあたりのサンプル数
    sound.writeframes(sound_frames)  # 音声データの書き込み

# wavの書き込み (scipyモジュール) -> お手軽！
sine_wave = sine_wave.astype(np.int16)  # 16bit整数に変換
wavfile.write(OUT_SCIPY_WAVE_FILE, n_framerate, sine_wave)
