#!/usr/bin/env python3

""" 音声情報処理 n本ノック !! """

# MIT License

# Copyright (C) 2020-2022 by Akira TAMAMORI

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
# - 畳み込みをスクラッチで実装する

import matplotlib.pyplot as plt
import numpy as np

# input signal
x = np.zeros(32, dtype=np.float32)
x[0], x[20] = 2.0, 1.0

# Impulse response (waves that decay while oscillating)
h = np.exp(- np.arange(16) / 4.0) * np.sin(2.0 * np.pi * np.arange(16) / 15.0)

# output signal
y = np.zeros(len(h) + len(x) - 1, dtype=np.float32)
hzero = np.hstack([h, np.zeros(len(x) - 1)])  # zero padding
xzero = np.hstack([x, np.zeros(len(h) - 1)])  # zero padding

# convolution
for n in range(0, len(y)):
    for k in range(0, n + 1):
        y[n] = y[n] + hzero[k] * xzero[n - k]

fig = plt.figure(figsize=(18, 4))
for i, (s, l) in enumerate(zip([x, h, y], ["input", "impulse response", "output"])):
    fig.add_subplot("13%d" % (i + 1))
    plt.plot(s, "-o", label=l)
    plt.xlim(0, len(y))
    plt.legend()
    plt.xlabel("Time index")
    plt.ylabel("Magnitude")
    plt.grid()

plt.show()

# numpy implementation
y_true = np.convolve(h, x, "full")
fig = plt.figure(figsize=(18, 4))
for i, (s, l) in enumerate(zip([x, h, y_true],
                               ["input", "impulse response (numpy)", "output"])):
    fig.add_subplot("13%d" % (i + 1))
    plt.plot(s, "-o", label=l)
    plt.xlim(0, len(y_true))
    plt.legend()
    plt.xlabel("Time index")
    plt.ylabel("Magnitude")
    plt.grid()

plt.show()
