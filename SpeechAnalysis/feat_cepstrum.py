#!/usr/bin/env python3

""" 音声情報処理 n本ノック !! """

# MIT License

# Copyright (C) 2021 by Akira TAMAMORI

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
# - ケプストラム法によりスペクトル包絡を抽出する
# - パワーが最大となる音声フレームを対象に推定

import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.io import wavfile

import librosa

IN_WAVE_FILE = "in.wav"  # 分析対象の音声

FRAME_LENGTH = 1024  # フレーム長 (FFTサイズ)
HOP_LENGTH = 80  # フレームのシフト長
FFT_LENGTH = FRAME_LENGTH

MAX_Fo = 200  # 分析における基本周波数の最大値 (Hz)
MIN_Fo = 60  # 分析における基本周波数の最小値 (Hz)

# 音声のロード
fs, data = wavfile.read(IN_WAVE_FILE)
data = data.astype(np.float64)

# ケプストラムの最大次数、最小次数
max_cep_order = int(np.floor(fs / MIN_Fo))
min_cep_order = int(np.floor(fs / MAX_Fo))

# フレーム化
frames = librosa.util.frame(data, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH).T

# パワーが最大のフレーム位置を取得
max_ind = np.argmax(np.sum(frames * frames, axis=1))

# パワーが最大となるフレームを取り出す
pow_max_frame = frames[max_ind, :]

# 窓掛け（ブラックマン窓）
window = scipy.signal.blackman(FFT_LENGTH)
windowed_frame = pow_max_frame * window

# ケプストラムの計算 (FFT → 絶対値2乗 → 対数 → 逆FFT)
fft_spec = scipy.fft.rfft(windowed_frame)
log_power = np.log(np.abs(fft_spec) ** 2)
cepstrum = scipy.fft.irfft(log_power).real
# real partを取るのはなぜ？→「対称性」を保証するため

# ケプストラム; 0次（直流）成分は外してプロット
plt.title("Cepstrum w/o DC")
n_samples = len(cepstrum)
quef = np.arange(FFT_LENGTH // 2 + 1) / fs
quef *= 1000  # to msec
plt.xlim([0, np.max(quef)])
plt.plot(quef, cepstrum[: len(quef)])
plt.xlabel("Quefrency (msec)")
plt.ylabel("Cepstrum")
plt.show()

lifter = 30  # リフタ次数
cepstrum[lifter : FFT_LENGTH - lifter + 1] = 0  # 高次ケプストラムを0にする
envelop = scipy.fft.rfft(cepstrum).real  # fftによりスペクトル包絡にする

# 対数パワースペクトル + スペクトル包絡
plt.title("Log power spectrum + spectral envelop")
plt.xlim([0, len(log_power)])
plt.plot(log_power, label="log power")
plt.plot(envelop, label="envelop")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Log power (dB)")
plt.show()
