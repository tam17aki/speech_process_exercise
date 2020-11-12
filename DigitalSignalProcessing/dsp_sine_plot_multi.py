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
# - ディジタルな正弦波を作成してプロットする
# - 離散時間でのサンプル点も分かりやすく表示する

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

samplerate = 1000000  # 標本化周波数（連続時間を表現するほど十分に大きくする）
duration = 0.001  # 音の継続時間 (sec)
amplitude = 1.0  # 正弦波の振幅
T = 1.0 / samplerate  # 標本化周期 (sec)

# 連続時間の正弦波
freq = 1000  # 正弦波の周波数 (Hz)
time = np.arange(0, duration + T, T)  # 継続時間に等しい標本点の作成
sine_wave = amplitude * np.sin(2 * np.pi * freq * time)

# 離散時間の正弦波
# 継続時間に等しい標本点の作成
sample_points = np.linspace(0, duration, num=17)
sample_sine = amplitude * np.sin(2 * np.pi * freq * sample_points)
f = interpolate.interp1d(sample_points, sample_sine, kind="linear")

# 連続時間の正弦波プロット
fig = plt.figure(figsize=(10, 10))
axes1 = fig.add_subplot(6, 1, 1)
axes1.plot(time, sine_wave, label="1000Hz")
axes1.set_ylabel("Amplitude")
axes1.set_title("Sine Wave")
axes1.plot(sample_points, sample_sine, "o")
axes1.plot(time, f(time), "r--", label="1000Hz")  # 離散時間の正弦波プロット
axes1.legend()

# 連続時間の正弦波
freq = 2000  # 正弦波の周波数 (Hz)
time = np.arange(0, duration + T, T)  # 継続時間に等しい標本点の作成
sine_wave = amplitude * np.sin(2 * np.pi * freq * time)

# 離散時間の正弦波
# 継続時間に等しい標本点の作成
sample_points = np.linspace(0, duration, num=17)
sample_sine = amplitude * np.sin(2 * np.pi * freq * sample_points)
f = interpolate.interp1d(sample_points, sample_sine, kind="linear")

# 連続時間の正弦波プロット
axes2 = fig.add_subplot(6, 1, 2)
axes2.plot(time, sine_wave, label="2000Hz")
axes2.set_ylabel("Amplitude")
axes2.plot(sample_points, sample_sine, "o")
axes2.plot(time, f(time), "r--", label="2000Hz")  # 離散時間の正弦波プロット
axes2.legend()

# 連続時間の正弦波
freq = 4000  # 正弦波の周波数 (Hz)
time = np.arange(0, duration + T, T)  # 継続時間に等しい標本点の作成
sine_wave = amplitude * np.sin(2 * np.pi * freq * time)

# 離散時間の正弦波
# 継続時間に等しい標本点の作成
sample_points = np.linspace(0, duration, num=17)
sample_sine = amplitude * np.sin(2 * np.pi * freq * sample_points)
f = interpolate.interp1d(sample_points, sample_sine, kind="linear")

# 連続時間の正弦波プロット
axes3 = fig.add_subplot(6, 1, 3)
axes3.plot(time, sine_wave, label="4000Hz")
axes3.set_ylabel("Amplitude")
axes3.plot(sample_points, sample_sine, "o")
axes3.plot(time, f(time), "r--", label="4000Hz")  # 離散時間の正弦波プロット
axes3.legend()

# 連続時間の正弦波
freq = 8000  # 正弦波の周波数 (Hz)
time = np.arange(0, duration + T, T)  # 継続時間に等しい標本点の作成
sine_wave = amplitude * np.sin(2 * np.pi * freq * time)

# 離散時間の正弦波
# 継続時間に等しい標本点の作成
sample_points = np.linspace(0, duration, num=17)
sample_sine = amplitude * np.sin(2 * np.pi * freq * sample_points)
f = interpolate.interp1d(sample_points, sample_sine, kind="linear")

# 連続時間の正弦波プロット
axes4 = fig.add_subplot(6, 1, 4)
axes4.plot(time, sine_wave, label="8000Hz")
axes4.set_ylabel("Amplitude")
axes4.plot(sample_points, sample_sine, "o")
axes4.plot(time, f(time), "r--", label="8000Hz")  # 離散時間の正弦波プロット
axes4.legend()

# 連続時間の正弦波
freq = 12000  # 正弦波の周波数 (Hz)
time = np.arange(0, duration + T, T)  # 継続時間に等しい標本点の作成
sine_wave = amplitude * np.sin(2 * np.pi * freq * time)

# 離散時間の正弦波
# 継続時間に等しい標本点の作成
sample_points = np.linspace(0, duration, num=17)
sample_sine = amplitude * np.sin(2 * np.pi * freq * sample_points)
f = interpolate.interp1d(sample_points, sample_sine, kind="linear")

# 連続時間の正弦波プロット
axes5 = fig.add_subplot(6, 1, 5)
axes5.plot(time, sine_wave, label="12000Hz")
axes5.set_ylabel("Amplitude")
axes5.plot(sample_points, sample_sine, "o")
axes5.plot(time, f(time), "r--", label="12000Hz")  # 離散時間の正弦波プロット
axes5.legend(loc="upper right")

# 連続時間の正弦波
freq = 16000  # 正弦波の周波数 (Hz)
time = np.arange(0, duration + T, T)  # 継続時間に等しい標本点の作成
sine_wave = amplitude * np.sin(2 * np.pi * freq * time)

# 離散時間の正弦波
# 継続時間に等しい標本点の作成
sample_points = np.linspace(0, duration, num=17)
sample_sine = amplitude * np.sin(2 * np.pi * freq * sample_points)
f = interpolate.interp1d(sample_points, sample_sine, kind="linear")

# 連続時間の正弦波プロット
axes6 = fig.add_subplot(6, 1, 6)
axes6.plot(time, sine_wave, label="16000Hz")
axes6.set_xlabel("Time (sec)")
axes6.set_ylabel("Amplitude")
axes6.plot(sample_points, sample_sine, "o")
axes6.plot(time, f(time), "r--", label="16000Hz")  # 離散時間の正弦波プロット
axes6.legend()

fig.tight_layout()
plt.savefig("dsp_sine_plot_multi.png")
plt.show()
