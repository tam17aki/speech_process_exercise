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
# - PySPTKによる音声の分析再合成 (MLSAフィルタ)
# - MLSAフィルタをボコーダー的に使って遊ぶ

from pysptk.synthesis import MLSADF, Synthesizer
from scipy.io import wavfile
import librosa
import numpy as np
import pysptk

FRAME_LENGTH = 1024
HOP_LENGTH = 80
MIN_F0 = 60
MAX_F0 = 240
ORDER = 25
ALPHA = 0.41

IN_WAVE_FILE = "in.wav"       # 入力音声

# 音声の読み込み
fs, x = wavfile.read(IN_WAVE_FILE)
x = x.astype(np.float64)

# 音声の切り出しと窓掛け
frames = librosa.util.frame(x, frame_length=FRAME_LENGTH,
                            hop_length=HOP_LENGTH).astype(np.float64).T
frames *= pysptk.blackman(FRAME_LENGTH)  # 窓掛け（ブラックマン窓）

# ピッチ抽出
pitch = pysptk.swipe(x, fs=fs, hopsize=HOP_LENGTH,
                     min=MIN_F0, max=MAX_F0, otype="pitch")

# 励振源信号(声帯音源)の生成
source_excitation = pysptk.excite(pitch, HOP_LENGTH)

# メルケプストラム分析（＝スペクトル包絡の抽出）
mc = pysptk.mcep(frames, ORDER, ALPHA)

# メルケプストラム係数からMLSAディジタルフィルタ係数に変換
mlsa_coef = pysptk.mc2b(mc, ALPHA)

# MLSAフィルタの作成
synthesizer = Synthesizer(MLSADF(order=ORDER, alpha=ALPHA), HOP_LENGTH)

# #### 以降、合成フィルタのパラメタなどを変えて色々な音声を合成

# ### ピッチシフト (音を高くする) ###
OUT_WAVE_FILE = "pitchshift_high.wav"
PITCH_SHIFT = 0.5               # 音を高くする場合は 1より小さい倍率
excitation_pitchhigh = pysptk.excite(pitch * PITCH_SHIFT, HOP_LENGTH)
y = synthesizer.synthesis(excitation_pitchhigh, mlsa_coef)  # 音声合成
y = y.astype(np.int16)
wavfile.write(OUT_WAVE_FILE, fs, y)

# ### ピッチシフト (音を低くする) ###
OUT_WAVE_FILE = "pitchshift_low.wav"
PITCH_SHIFT = 1.5               # 音を低くする場合は 1より大きい倍率
excitation_pitchlow = pysptk.excite(pitch * PITCH_SHIFT, HOP_LENGTH)
y = synthesizer.synthesis(excitation_pitchlow, mlsa_coef)
y = y.astype(np.int16)
wavfile.write(OUT_WAVE_FILE, fs, y)

# ### テンポ変更 (再生時間を短くする)
OUT_WAVE_FILE = "tempo_fast.wav"
HOP_LENGTH_FAST = int(HOP_LENGTH * 0.5)
synthesizer_fast = Synthesizer(
    MLSADF(order=ORDER, alpha=ALPHA), HOP_LENGTH_FAST)
excitation_fast = pysptk.excite(pitch, HOP_LENGTH_FAST)
y = synthesizer_fast.synthesis(excitation_fast, mlsa_coef)
y = y.astype(np.int16)
wavfile.write(OUT_WAVE_FILE, fs, y)

# ### テンポ変更 (再生時間を長くする)
OUT_WAVE_FILE = "tempo_slow.wav"
HOP_LENGTH_SLOW = int(HOP_LENGTH * 2.0)
synthesizer_slow = Synthesizer(
    MLSADF(order=ORDER, alpha=ALPHA), HOP_LENGTH_SLOW)
excitation_slow = pysptk.excite(pitch, HOP_LENGTH_SLOW)
y = synthesizer_slow.synthesis(excitation_slow, mlsa_coef)
y = y.astype(np.int16)
wavfile.write(OUT_WAVE_FILE, fs, y)

# ### かすれ声（白色雑音で駆動）
OUT_WAVE_FILE = "hoarse.wav"
PITCH_RATE = 0.0               # 0.0にすることで強制的に無声音にする
excitation_hoarse = pysptk.excite(pitch * PITCH_RATE, HOP_LENGTH)
y = synthesizer.synthesis(excitation_hoarse, mlsa_coef)
y = y.astype(np.int16)
wavfile.write(OUT_WAVE_FILE, fs, y)

# ### ロボット声（抑揚がない）
OUT_WAVE_FILE = "robot.wav"
robot_f0 = 150                  # 150 Hz
pitch_robot = np.ones(len(pitch)) * (fs / robot_f0)
excitation_robot = pysptk.excite(pitch_robot, HOP_LENGTH)
y = synthesizer.synthesis(excitation_robot, mlsa_coef)
y = y.astype(np.int16)
wavfile.write(OUT_WAVE_FILE, fs, y)

# ### 子供の声（声道を短くする）
OUT_WAVE_FILE = "child.wav"
ALPHA_CHILD = 0.2
PITCH_SHIFT = 0.5
excitation_pitchhigh = pysptk.excite(pitch * PITCH_SHIFT, HOP_LENGTH)
synthesizer_child = Synthesizer(MLSADF(order=ORDER, alpha=ALPHA_CHILD),
                                HOP_LENGTH)
y = synthesizer_child.synthesis(excitation_pitchhigh, mlsa_coef)
y = y.astype(np.int16)
wavfile.write(OUT_WAVE_FILE, fs, y)

# ### 太い大人の声（声道を長くする）
OUT_WAVE_FILE = "adult.wav"
ALPHA_ADULT = 0.6
PITCH_SHIFT = 1.5
excitation_pitchlow = pysptk.excite(pitch * PITCH_SHIFT, HOP_LENGTH)
synthesizer_child = Synthesizer(MLSADF(order=ORDER, alpha=ALPHA_ADULT),
                                HOP_LENGTH)
y = synthesizer_child.synthesis(excitation_pitchlow, mlsa_coef)
y = y.astype(np.int16)
wavfile.write(OUT_WAVE_FILE, fs, y)
