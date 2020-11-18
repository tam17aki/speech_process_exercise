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
# MFCCの抽出と可視化 by librosa
# 波形読み込みはscipy.ioのwavfileモジュール

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

IN_WAVE_FILE = "in.wav"  # モノラル音声（前提）

FRAME_LENGTH = 1024  # フレーム長
HOP_LENGTH = 80  # フレームのシフト長
N_MELS = 128  # メルフィルタバンクの数
N_MFCC = 20  # MFCCの次数

# 音声データ読み込み (fsがサンプリング周波数、dataは音声データ)
fs, data = wavfile.read(IN_WAVE_FILE)
data = data.astype(np.float64)

# MFCCの抽出 (音声から抽出)
mfcc = librosa.feature.mfcc(y=data, sr=fs, n_mels=N_MELS, hop_length=HOP_LENGTH)

# 形状の確認
print("MFCC arrayの形状: ", mfcc.shape)

# MFCCの表示
fig = plt.figure(figsize=(10, 4))
librosa.display.specshow(mfcc, x_axis="time", hop_length=HOP_LENGTH, sr=fs)
plt.colorbar()
plt.tight_layout()
plt.show()

# メルスペクトログラムの抽出
mel_spec = librosa.feature.melspectrogram(
    y=data, sr=fs, n_mels=N_MELS, hop_length=HOP_LENGTH
)

# デシベルスケールにする
mel_spec_dB = librosa.power_to_db(mel_spec, ref=np.max)

# MFCCの抽出
mfcc = librosa.feature.mfcc(S=mel_spec_dB, sr=fs, n_mels=N_MELS, hop_length=HOP_LENGTH)

# メルスペクトログラムの表示
fig = plt.figure(figsize=(10, 4))
librosa.display.specshow(mfcc, x_axis="time", hop_length=HOP_LENGTH, sr=fs)
plt.colorbar()
plt.tight_layout()
plt.show()
