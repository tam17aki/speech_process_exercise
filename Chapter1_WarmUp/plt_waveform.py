#!/usr/bin/env python3

""" 音声情報処理 n本ノック !! """

# Copyright (C) 2020 by Akira TAMAMORI

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Commentary:
# matplotlib を用いた波形プロット

from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

IN_WAVE_FILE = "in.wav"  # モノラル音声（前提）

# 波形表示
fs, data = wavfile.read(IN_WAVE_FILE)
n_samples = len(data)
time = np.arange(n_samples) / fs
plt.plot(time, data)
plt.xlabel("Time (sec)")
plt.ylabel("Amplitude")
plt.title("Waveform")
plt.show()
