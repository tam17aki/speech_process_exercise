#!/usr/bin/env python3

""" 音声情報処理 n本ノック !! """

# MIT License

# Copyright (c) 2019 Yoshiki Masuyama

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
# Masuyama 氏らの提案手法に基づく位相復元 (便宜的にADMM法とする):
#
# Y. Masuyama, K. Yatabe and Y. Oikawa, "Griffin-Lim like phase
# recovery via alternating direction method of multipliers," IEEE
# Signal Processing Letters, vol.26, no.1, pp.184--188, Jan. 2019.
# https://ieeexplore.ieee.org/document/8552369

import numpy as np
from scipy.io import wavfile
import librosa

IN_WAVE_FILE = "in.wav"  # モノラル音声
OUT_WAVE_FILE = "out_admm_gla.wav"  # 復元音声

FRAME_LENGTH = 1024        # フレーム長 (FFTサイズ)
HOP_LENGTH = 80            # フレームのシフト長

ITERATION = 200            # 位相推定の最大繰り返し数

MULTIPLIER = 0.01          # ADMM法の強さを制御; 0.0のときはGriffin-Lim法に一致

# 音声のロード
fs, data = wavfile.read(IN_WAVE_FILE)
data = data.astype(np.float64)

# 振幅スペクトル（位相復元なので手に入るのはこれのみ）
amp_spec = np.abs(librosa.core.stft(data, n_fft=FRAME_LENGTH,
                                    hop_length=HOP_LENGTH,
                                    win_length=FRAME_LENGTH))

# ADMM法に基づく位相スペクトルの推定
for i in range(ITERATION):
    if i == 0:
        # 初回は乱数で初期化
        phase_spec = np.random.rand(*amp_spec.shape)
        control_spec = np.zeros(amp_spec.shape)
    else:
        # 振幅スペクトルと推定された位相スペクトルから複素スペクトログラムを復元
        recovered_spec = amp_spec * np.exp(1j * phase_spec)

        # 短時間フーリエ逆変換で音声を復元
        combined = recovered_spec + control_spec
        recovered = librosa.core.istft(combined, hop_length=HOP_LENGTH,
                                       win_length=FRAME_LENGTH)

        # 復元音声から複素スペクトログラムを再計算
        complex_spec = librosa.core.stft(recovered, n_fft=FRAME_LENGTH,
                                         hop_length=HOP_LENGTH,
                                         win_length=FRAME_LENGTH)
        complex_spec = MULTIPLIER * combined + complex_spec
        complex_spec /= (1.0 + MULTIPLIER)

        # 初回以降は計算済みの複素スペクトログラムから位相スペクトルを推定
        control_spec = control_spec + recovered_spec - complex_spec
        phase_spec = np.angle(complex_spec - control_spec)

# 音声を復元
recovered_spec = amp_spec * np.exp(1j * phase_spec)
recovered = librosa.core.istft(recovered_spec, hop_length=HOP_LENGTH,
                               win_length=FRAME_LENGTH)
recovered = recovered.astype(np.int16)

# 復元された音声をwavファイルとして保存
wavfile.write(OUT_WAVE_FILE, fs, recovered)
