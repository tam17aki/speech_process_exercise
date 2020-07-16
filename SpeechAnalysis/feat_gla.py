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
# - Griffin-Lim法により位相を復元する

import numpy as np
from scipy.io import wavfile
import librosa

IN_WAVE_FILE = "in.wav"  # モノラル音声
OUT_WAVE_FILE = "out_gla.wav"  # 復元音声

FRAME_LENGTH = 1024             # フレーム長 (FFTサイズ)
HOP_LENGTH = 80                 # フレームのシフト長

ITERATION = 200                 # Griffin-Lim法における位相推定の最大繰り返し数

# 音声のロード
fs, data = wavfile.read(IN_WAVE_FILE)

# フレーム分析で余りが出ないようにする
n_frames = (len(data) - FRAME_LENGTH) / HOP_LENGTH
n_frames = int(np.floor(n_frames)) if n_frames >= 0 else int(np.ceil(n_frames))
data = data[:FRAME_LENGTH + n_frames * HOP_LENGTH]
data = data.astype(np.float64)

# 振幅スペクトル（位相復元なので手に入るのはこれのみ）
amp_spec = np.abs(librosa.core.stft(data, n_fft=FRAME_LENGTH,
                                    hop_length=HOP_LENGTH,
                                    win_length=FRAME_LENGTH))

# Griffin-Lim法に基づく位相スペクトルの推定
for i in range(ITERATION):
    if i == 0:
        # 初回は乱数で初期化
        phase_spec = np.random.rand(*amp_spec.shape)
    else:
        # 振幅スペクトルと推定された位相スペクトルから複素スペクトログラムを復元
        recovered_spec = amp_spec * np.exp(1j * phase_spec)

        # 短時間フーリエ逆変換で音声を復元
        recovered = librosa.core.istft(recovered_spec, hop_length=HOP_LENGTH,
                                       win_length=FRAME_LENGTH)
        # 復元音声から複素スペクトログラムを再計算
        complex_spec = librosa.core.stft(recovered, n_fft=FRAME_LENGTH,
                                         hop_length=HOP_LENGTH,
                                         win_length=FRAME_LENGTH)

        # 初回以降は計算済みの複素スペクトログラムから位相スペクトルを推定
        phase_spec = np.angle(complex_spec)

# 音声を復元
recovered_spec = amp_spec * np.exp(1j * phase_spec)
recovered = librosa.core.istft(recovered_spec, hop_length=HOP_LENGTH,
                               win_length=FRAME_LENGTH)
recovered = recovered.astype(np.int16)

# 復元された音声をwavファイルとして保存
wavfile.write(OUT_WAVE_FILE, fs, recovered)
