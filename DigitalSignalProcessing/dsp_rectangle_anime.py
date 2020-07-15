#!/usr/bin/env python

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
# - 矩形波をフーリエ級数近似により作成する
# - 近似の様子をアニメーションにより可視化


import math
import numpy
import numpy.matlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Period [s]
PERIOD = 1

# Sampling frequency for plot
SAMP_FREQ = 100

# Duration[s]
TIME_LEN = 4 * PERIOD  #
TIME_NUM = math.floor(TIME_LEN * SAMP_FREQ)  # 400

# Angle [rad]
ANGLE = numpy.linspace(0, 2 * math.pi, SAMP_FREQ)  # (100, 1)

# Order of Fourier Series
ORDER = numpy.array([1, 3, 5, 7, 9])
ORDER_MAT = numpy.matlib.repmat(ORDER, TIME_NUM, 1)  # (400, 5)

X_MAX = 1.2
Y_MAX = 1.2
X_MIN = -1.2
Y_MIN = -1.2

fig = plt.figure(figsize=[8.0, 8.0])  # 800 x 800
ax1 = fig.add_axes([0.04, 0.85, 0.14, 0.14])
ax1.set_xlim(X_MIN, X_MAX)
ax1.set_ylim(Y_MIN, Y_MAX)

ax2 = fig.add_axes([0.24, 0.85, 0.74, 0.14])
ax2.set_ylim(Y_MIN, Y_MAX)

ax3 = fig.add_axes([0.04, 0.65, 0.14, 0.14])
ax3.set_xlim(X_MIN, X_MAX)
ax3.set_ylim(Y_MIN, Y_MAX)

ax4 = fig.add_axes([0.24, 0.65, 0.74, 0.14])
ax4.set_ylim(Y_MIN, Y_MAX)

ax5 = fig.add_axes([0.04, 0.45, 0.14, 0.14])
ax5.set_xlim(X_MIN, X_MAX)
ax5.set_ylim(Y_MIN, Y_MAX)

ax6 = fig.add_axes([0.24, 0.45, 0.74, 0.14])
ax6.set_ylim(Y_MIN, Y_MAX)

ax7 = fig.add_axes([0.04, 0.25, 0.14, 0.14])
ax7.set_xlim(X_MIN, X_MAX)
ax7.set_ylim(Y_MIN, Y_MAX)

ax8 = fig.add_axes([0.24, 0.25, 0.74, 0.14])
ax8.set_ylim(Y_MIN, Y_MAX)

ax9 = fig.add_axes([0.24, 0.05, 0.74, 0.14])
ax9.set_ylim(Y_MIN, Y_MAX)

images = []

for t0 in range(TIME_NUM):

    # Time [s]
    time_axis = numpy.arange(0, TIME_NUM).T / SAMP_FREQ  # (400, )
    time_axis = time_axis[::-1]
    t = numpy.arange(t0, t0 + TIME_NUM).T / SAMP_FREQ  # (400, )
    t = numpy.expand_dims(t, axis=1)  # (400, 1)
    t_mat = numpy.matlib.repmat(t, 1, len(ORDER))  # (400, 5)

    # Fourier coefficients
    coef = 2 * PERIOD / (math.pi * ORDER) * \
        numpy.cos(math.pi * ORDER)  # Saw wav
    # coef = -PERIOD / (math.pi * ORDER) * numpy.cos(math.pi * ORDER)  # Saw wave

    # phase on the circumference
    phi = 2 * math.pi * ORDER_MAT * t_mat / PERIOD  # (400, 5)

    # unit circle
    circ = numpy.array([coef * numpy.cos(phi[TIME_NUM-1, :]),
                        coef * numpy.sin(phi[TIME_NUM-1, :])])  # (2, 5, 5)

    sig = numpy.sum(numpy.matlib.repmat(
        coef, TIME_NUM, 1) * numpy.sin(phi), axis=1)

    # plot complex plane k=1
    im = ax1.plot(coef[0] * numpy.cos(ANGLE), coef[0] * numpy.sin(ANGLE),
                  color="k", linewidth=1.5)
    im += ax1.plot([0, circ[0, 0]], [0, circ[1, 0]],
                   linestyle="-", color="b", marker="o",
                   markerfacecolor="b", markersize=4)
    im += ax1.plot([circ[0, 0], X_MAX], [circ[1, 0], circ[1, 0]],
                   linestyle=":", color="b", marker="o", markersize=4,
                   markerfacecolor="b", linewidth=1)

    # plot signal k=1
    im += ax2.plot(time_axis, coef[0] * numpy.sin(phi[:, 0]),
                   linestyle="-", color="b", linewidth=1.5)

    # plot complex plane k = 2
    im += ax3.plot(coef[0] * numpy.cos(ANGLE), coef[0] * numpy.sin(ANGLE),
                   color="k", linewidth=1.5)
    im += ax3.plot(coef[1] * numpy.cos(ANGLE) + circ[0, 0],
                   coef[1] * numpy.sin(ANGLE) + circ[1, 0],
                   color="k", linewidth=1.5)
    im += ax3.plot([0, circ[0, 0]], [0, circ[1, 0]],
                   color="b", linestyle="-", marker="o",
                   markerfacecolor="b", markersize=4)
    im += ax3.plot([circ[0, 0], circ[0, 1] + circ[0, 0]],
                   [circ[1, 0], circ[1, 1] + circ[1, 0]],
                   color="b", linestyle="-", marker="o",
                   markerfacecolor="b", markersize=4)
    im += ax3.plot([circ[0, 1] + circ[0, 0], X_MAX],
                   [circ[1, 1] + circ[1, 0], circ[1, 1] + circ[1, 0]],
                   color="b", linestyle=":", marker="o", markerfacecolor="b",
                   linewidth=1, markersize=4)
    # plot signal k = 2
    im += ax4.plot(time_axis,
                   coef[1] * numpy.sin(phi[:, 1]) +
                   coef[0] * numpy.sin(phi[:, 0]),
                   linestyle="-", color="b", linewidth=1.5)

    # plot complex plane k = 3
    im += ax5.plot(coef[0] * numpy.cos(ANGLE), coef[0] * numpy.sin(ANGLE),
                   color="k", linewidth=1.5)
    im += ax5.plot(coef[1] * numpy.cos(ANGLE) + circ[0, 0],
                   coef[1] * numpy.sin(ANGLE) + circ[1, 0],
                   color="k", linewidth=1.5)
    im += ax5.plot(coef[2] * numpy.cos(ANGLE) + circ[0, 0] + circ[0, 1],
                   coef[2] * numpy.sin(ANGLE) + circ[1, 0] + circ[1, 1],
                   color="k", linewidth=1.5)
    im += ax5.plot([0, circ[0, 0]], [0, circ[1, 0]],
                   color="b", linestyle="-", marker="o",
                   markerfacecolor="b", markersize=4)
    im += ax5.plot([circ[0, 0], circ[0, 1] + circ[0, 0]],
                   [circ[1, 0], circ[1, 1] + circ[1, 0]],
                   color="b", linestyle="-", marker="o",
                   markerfacecolor="b", markersize=4)
    im += ax5.plot([circ[0, 1] + circ[0, 0], circ[0, 2] + circ[0, 1] + circ[0, 0]],
                   [circ[1, 1] + circ[1, 0], circ[1, 2] + circ[1, 1] + circ[1, 0]],
                   color="b", linestyle="-", marker="o",
                   markerfacecolor="b", markersize=4)
    im += ax5.plot([circ[0, 2] + circ[0, 1] + circ[0, 0], X_MAX],
                   [circ[1, 2] + circ[1, 1] + circ[1, 0],
                    circ[1, 2] + circ[1, 1] + circ[1, 0]],
                   color="b", linestyle=":", marker="o", markerfacecolor="b",
                   linewidth=1, markersize=4)

    # plot signal k = 3
    im += ax6.plot(time_axis, coef[2] * numpy.sin(phi[:, 2])
                   + coef[1] * numpy.sin(phi[:, 1])
                   + coef[0] * numpy.sin(phi[:, 0]),
                   linestyle="-", color="b", linewidth=1.5)

    # plot complex plane k = 4
    im += ax7.plot(coef[0] * numpy.cos(ANGLE), coef[0] * numpy.sin(ANGLE),
                   color="k", linewidth=1.5)
    im += ax7.plot(coef[1] * numpy.cos(ANGLE) + circ[0, 0],
                   coef[1] * numpy.sin(ANGLE) + circ[1, 0],
                   color="k", linewidth=1.5)
    im += ax7.plot(coef[2] * numpy.cos(ANGLE) + circ[0, 0] + circ[0, 1],
                   coef[2] * numpy.sin(ANGLE) + circ[1, 0] + circ[1, 1],
                   color="k", linewidth=1.5)
    im += ax7.plot(coef[3] * numpy.cos(ANGLE) + circ[0, 0] + circ[0, 1] + circ[0, 2],
                   coef[3] * numpy.sin(ANGLE) + circ[1, 0] +
                   circ[1, 1] + circ[1, 2],
                   color="k", linewidth=1.5)
    im += ax7.plot([0, circ[0, 0]], [0, circ[1, 0]],
                   color="b", linestyle="-", marker="o",
                   markerfacecolor="b", markersize=4)
    im += ax7.plot([circ[0, 0], circ[0, 1] + circ[0, 0]],
                   [circ[1, 0], circ[1, 1] + circ[1, 0]],
                   color="b", linestyle="-", marker="o",
                   markerfacecolor="b", markersize=4)
    im += ax7.plot([circ[0, 1] + circ[0, 0], circ[0, 2] + circ[0, 1] + circ[0, 0]],
                   [circ[1, 1] + circ[1, 0], circ[1, 2] + circ[1, 1] + circ[1, 0]],
                   color="b", linestyle="-", marker="o",
                   markerfacecolor="b", markersize=4)
    im += ax7.plot([circ[0, 2] + circ[0, 1] + circ[0, 0],
                    circ[0, 3] + circ[0, 2] + circ[0, 1] + circ[0, 0]],
                   [circ[1, 2] + circ[1, 1] + circ[1, 0],
                    circ[1, 3] + circ[1, 2] + circ[1, 1] + circ[1, 0]],
                   color="b", linestyle="-", marker="o",
                   markerfacecolor="b", markersize=4)
    im += ax7.plot([circ[0, 3] + circ[0, 2] + circ[0, 1] + circ[0, 0], X_MAX],
                   [circ[1, 3] + circ[1, 2] + circ[1, 1] + circ[1, 0],
                    circ[1, 3] + circ[1, 2] + circ[1, 1] + circ[1, 0]],
                   color="b", linestyle=":", marker="o", markerfacecolor="b",
                   linewidth=1, markersize=4)

    # plot signal
    im += ax8.plot(time_axis, coef[3] * numpy.sin(phi[:, 3])
                   + coef[2] * numpy.sin(phi[:, 2])
                   + coef[1] * numpy.sin(phi[:, 1])
                   + coef[0] * numpy.sin(phi[:, 0]),
                   linestyle="-", color="b", linewidth=1.5)

    # plot signal
    rectwave = -0.5 * numpy.sign(numpy.sin(2 * math.pi * t / PERIOD))
    im += ax9.plot(time_axis, rectwave, linestyle="-",
                   color="b", linewidth=1.5)

    images.append(im)

ANIME = animation.ArtistAnimation(fig, images, interval=40)
ANIME.save("rectangle_anime.mp4", writer="ffmpeg", dpi=300)
