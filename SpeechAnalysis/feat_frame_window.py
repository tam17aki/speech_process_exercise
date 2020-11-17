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
# - librosaによるフレーム化処理
# - scipy.signalによる窓掛け

import librosa
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.io import wavfile

FRAME_LENGTH = 1024  # フレーム長
HOP_LENGTH = 80  # フレームシフト

IN_WAVE_FILE = "in.wav"  # 入力音声

# 音声の読み込み
fs, x = wavfile.read(IN_WAVE_FILE)
x = x.astype(np.float64)

# 音声のフレーム化
frames = librosa.util.frame(x, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)
# frame関数は (フレーム長, フレーム数)で返すので、(フレーム数, フレーム長)に転置
frames = frames.astype(np.float64).T

# 窓掛け（ブラックマン窓）
window = signal.blackman(FRAME_LENGTH)
frames_after = frames * window

# 窓掛け前後の音声波形を観察
frame_number = 100  # 第100フレーム
plt.figure(figsize=(8, 4))
plt.plot(frames[frame_number, :], label="before windowed")
plt.plot(frames_after[frame_number, :], label="after windowed")
plt.legend()
plt.show()
