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
# - Pyroomacousticsを用いたILRMAベースの音源分離デモ

import os

import matplotlib.pyplot as plt
import numpy as np
import pyroomacoustics as pra
from scipy import signal
from scipy.io import wavfile

INDIR = "./input"
SRC_WAV1 = INDIR + "/drums.wav"
SRC_WAV2 = INDIR + "/piano.wav"
OUTDIR = "./output/ILRMA"
os.makedirs(OUTDIR, exist_ok=True)

fsResample = 16000  # リサンプリングの周波数 (Hz)
FFT_LENGTH = 4096  # STFT時のFFT長 (points)
HOP_LENGTH = 2048  # STFT時のフレームシフト長 (points)
N_SOURCES = 2  # 音源数
N_ITER = 100  # ILRMAにおける推定回数（内部パラメタ）
N_BASES = 10  # ILRMAにおける基底数（内部パラメタ）

# ### 混合音の作成 ###
# sig: signal x channel x source という3次元アレイ
fs, sig_src1 = wavfile.read(SRC_WAV1)
fs, sig_src2 = wavfile.read(SRC_WAV2)
sig_src2 = sig_src2[: len(sig_src1)]
sig = np.stack([sig_src1, sig_src2], axis=1)

# 元の音源をリサンプリング (多項式補完)
sig_src1 = signal.resample_poly(sig[:, :, 0], fsResample, fs)
sig_src2 = signal.resample_poly(sig[:, :, 1], fsResample, fs)
sig_resample = np.stack([sig_src1, sig_src2], axis=1)

# 混合信号を作成
# 各チャネルごとに、音源の足し算
mix1 = sig_resample[:, 0, 0] + sig_resample[:, 0, 1]  # 第0チャネル (left)
mix2 = sig_resample[:, 1, 0] + sig_resample[:, 1, 1]  # 第1チャネル (right)
mixed = np.stack([mix1, mix2], axis=1)

# ### 音源分離の実行 ###
# 分析窓
win_a = pra.hamming(FFT_LENGTH)

# 合成窓: 分析窓を事前に並べておく
win_s = pra.transform.compute_synthesis_window(win_a, HOP_LENGTH)

# 短時間フーリエ変換によるスペクトログラム作成
X = pra.transform.analysis(mixed, FFT_LENGTH, HOP_LENGTH, win=win_a)

# ILRMA適用
Y = pra.bss.ilrma(X, n_src=N_SOURCES, n_iter=N_ITER, n_components=N_BASES)

# 逆短時間フーリエ変換により音声に戻す
y = pra.transform.synthesis(Y, FFT_LENGTH, HOP_LENGTH, win=win_s)

# ### スペクトログラムの表示 ###
# 分離前の音源
fig = plt.figure(figsize=(8, 6))  # プロット枠を確保
axes1 = fig.add_subplot(2, 1, 1)
axes2 = fig.add_subplot(2, 1, 2)
axes1.specgram(
    (sig_resample[:, 0, 0] + sig_resample[:, 1, 0]) * 0.5,
    NFFT=FFT_LENGTH,
    noverlap=HOP_LENGTH,
    Fs=fsResample,
    cmap="jet",
)
axes1.set_xlabel("Time (sec)")  # x軸のラベル
axes1.set_ylabel("Frequency (Hz)")  # y軸のラベル
axes1.set_title("Spectrogram (Source 1)")  # 画像のタイトル
axes2.specgram(
    (sig_resample[:, 0, 1] + sig_resample[:, 1, 1]) * 0.5,
    NFFT=FFT_LENGTH,
    noverlap=HOP_LENGTH,
    Fs=fsResample,
    cmap="jet",
)
axes2.set_xlabel("Time (sec)")  # x軸のラベル
axes2.set_ylabel("Frequency (Hz)")  # y軸のラベル
axes2.set_title("Spectrogram (Source 2)")  # 画像のタイトル
plt.tight_layout()
plt.show()  # 画像を画面表示

# audio

# 混合音源
plt.figure(figsize=(10, 4))
plt.specgram(
    (mixed[:, 0] + mixed[:, 1]) * 0.5,  # 2ch -> 1ch
    NFFT=FFT_LENGTH,
    noverlap=HOP_LENGTH,
    Fs=fsResample,
    cmap="jet",
)
plt.xlabel("Time (sec)")  # x軸のラベル
plt.ylabel("Frequency (Hz)")  # y軸のラベル
plt.title("Spectrogram (Mixed)")  # 画像のタイトル
plt.tight_layout()
plt.show()  # 画像を画面表示

# audio

# 分離後の音源
fig = plt.figure(figsize=(8, 6))  # プロット枠を確保
axes1 = fig.add_subplot(2, 1, 1)
axes2 = fig.add_subplot(2, 1, 2)
axes1.specgram(
    y[:, 1], NFFT=FFT_LENGTH, noverlap=HOP_LENGTH, Fs=fsResample, cmap="jet",
)
axes1.set_xlabel("Time (sec)")  # x軸のラベル
axes1.set_ylabel("Frequency (Hz)")  # y軸のラベル
axes1.set_title("Spectrogram (Source 1)")  # 画像のタイトル
axes2.specgram(
    y[:, 0], NFFT=FFT_LENGTH, noverlap=HOP_LENGTH, Fs=fsResample, cmap="jet",
)
axes2.set_xlabel("Time (sec)")  # x軸のラベル
axes2.set_ylabel("Frequency (Hz)")  # y軸のラベル
axes2.set_title("Spectrogram (Source 2)")  # 画像のタイトル
plt.tight_layout()
plt.show()  # 画像を画面表示

# 型変換
mixed = mixed * np.iinfo(np.int16).max
mixed = mixed.astype(np.int16)
sig_resample = sig_resample * np.iinfo(np.int16).max
sig_resample = sig_resample.astype(np.int16)
y = y * np.iinfo(np.int16).max
y = y.astype(np.int16)

# ### 各種音源の保存
# mixed signal (observation)
wavfile.write("{}/mixed.wav".format(OUTDIR), fsResample, mixed)

# source signal 1
wavfile.write(
    "{}/source1.wav".format(OUTDIR),
    fsResample,
    (sig_resample[:, 0, 0] * sig_resample[:, 1, 0]) * 0.5,
)

# source signal 2
wavfile.write(
    "{}/source2.wav".format(OUTDIR),
    fsResample,
    (sig_resample[:, 0, 1] * sig_resample[:, 1, 1]) * 0.5,
)

# estimated signal 1
wavfile.write("{}/estimated1.wav".format(OUTDIR), fsResample, y[:, 0])

# estimated signal 2
wavfile.write("{}/estimated2.wav".format(OUTDIR), fsResample, y[:, 1])
