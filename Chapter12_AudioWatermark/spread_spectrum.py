#!/usr/bin/env python3

"""A python script to perform audio watermark embedding/detection
   on the basis of direct-sequence spread spectrum method."""

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

import numpy as np
from scipy.io import wavfile

HOST_SIGNAL_FILE = "host.wav"                       # 透かし埋め込み先のファイル
WATERMARK_SIGNAL_FILE = "wmed_signal.wav"           # 透かしを埋め込んだファイル
PSEUDO_RAND_FILE = 'pseudo_rand.dat'                # 疑似乱数列のファイル
WATERMARK_ORIGINAL_FILE = 'watermark_ori.dat'       # オリジナルの透かし信号
WATERMARK_EXTENDED_FILE = 'watermark_extended.dat'  # 拡張透かし信号

REP_CODE = True                 # 繰り返し埋め込みを使う
FRAME_LENGTH = 1024             # フレーム長
CONTROL_STRENGTH = 0.03         # 埋め込み強度
OVERLAP = 0.0                   # フレーム分析のオーバーラップ率
NUM_REPS = 3                    # 埋め込みの繰り返し数


def fix(xs):
    """
    A emuration of MATLAB 'fix' function.
    borrowed from https://ideone.com/YjJwOh
    """

    if xs >= 0:
        res = np.floor(xs)
    else:
        res = np.ceil(xs)
    return res


def embed():
    """ Embed watermark."""

    # 疑似乱数系列を生成 (pseudo random sequence; PRS)
    prs = np.random.rand(1, FRAME_LENGTH) - 0.5

    # 疑似乱数系列を保存
    with open(PSEUDO_RAND_FILE, 'w') as f:
        for d in np.squeeze(prs):
            f.write("%f\n" % d)

    # 埋め込み先の音声ファイルを開く
    sr, host_signal = wavfile.read(HOST_SIGNAL_FILE)
    signal_len = len(host_signal)

    # フレームの移動量 (hop_length)
    frame_shift = int(FRAME_LENGTH * (1 - OVERLAP))

    # 隣接フレームとのオーバーラップ長
    overlap_length = int(FRAME_LENGTH * OVERLAP)

    # 埋め込み可能なビット数
    embed_nbit = fix((signal_len - overlap_length) / frame_shift)

    if REP_CODE:
        # 実質的な埋め込み可能ビット数
        effective_nbit = np.floor(embed_nbit / NUM_REPS)

        embed_nbit = effective_nbit * NUM_REPS
    else:
        effective_nbit = embed_nbit

    # 整数化
    frame_shift = int(frame_shift)
    effective_nbit = int(effective_nbit)
    embed_nbit = int(embed_nbit)

    # オリジナルの透かし信号を作成（0と1のビット列）
    wmark_original = np.random.randint(2, size=int(effective_nbit))

    # オリジナルの透かし信号を保存
    with open(WATERMARK_ORIGINAL_FILE, 'w') as f:
        for d in wmark_original:
            f.write("%d\n" % d)

    # 透かし信号を拡張する
    if REP_CODE:
        wmark_extended = np.repeat(wmark_original, NUM_REPS)
    else:
        wmark_extended = wmark_original

    # 拡張された透かし信号を保存する
    with open(WATERMARK_EXTENDED_FILE, 'w') as f:
        for d in np.squeeze(wmark_extended):
            f.write("%f\n" % d)

    # 透かしが埋め込まれた信号(watermarked signal)を生成
    pointer = 0
    wmed_signal = np.zeros((frame_shift * embed_nbit))  # watermarked signal
    for i in range(embed_nbit):
        frame = host_signal[pointer: (pointer + FRAME_LENGTH)]

        alpha = CONTROL_STRENGTH * np.max(np.abs(frame))

        # ビット値に応じて情報を埋め込む
        if wmark_extended[i] == 1:
            frame = frame + alpha * prs
        else:
            frame = frame - alpha * prs

        wmed_signal[frame_shift * i: frame_shift * (i+1)] = \
            frame[0, 0:frame_shift]

        pointer = pointer + frame_shift

    wmed_signal = np.concatenate(
        (wmed_signal, host_signal[len(wmed_signal): signal_len]))

    # 透かしが埋め込まれた信号をwavとして保存
    wmed_signal = wmed_signal.astype(np.int16)  # convert float into integer
    wavfile.write(WATERMARK_SIGNAL_FILE, sr, wmed_signal)


def detect():
    """ Detect watermark."""

    # 埋め込み先の音声ファイルを開く
    _, host_signal = wavfile.read(HOST_SIGNAL_FILE)

    # 埋め込み済みの音声ファイルを開く
    _, eval_signal = wavfile.read(WATERMARK_SIGNAL_FILE)
    signal_len = len(eval_signal)

    frame_shift = FRAME_LENGTH * (1 - OVERLAP)
    embed_nbit = fix((signal_len - FRAME_LENGTH * OVERLAP) / frame_shift)

    if REP_CODE:
        # 実質的な埋め込み可能ビット数
        effective_nbit = np.floor(embed_nbit / NUM_REPS)

        embed_nbit = effective_nbit * NUM_REPS
    else:
        effective_nbit = embed_nbit

    frame_shift = int(frame_shift)
    effective_nbit = int(effective_nbit)
    embed_nbit = int(embed_nbit)

    # オリジナルの透かし信号をロード
    with open(WATERMARK_ORIGINAL_FILE, 'r') as f:
        wmark_original = f.readlines()
    wmark_original = np.array([int(w.rstrip()) for w in wmark_original])

    # 透かし埋め込みに用いた擬似乱数列をロード
    with open(PSEUDO_RAND_FILE, 'r') as f:
        prs = f.readlines()
    rr = np.array([float(x.rstrip()) for x in prs])

    pointer = 0
    detected_bit = np.zeros(embed_nbit)
    for i in range(embed_nbit):
        frame = eval_signal[pointer: pointer + FRAME_LENGTH] - \
            host_signal[pointer: pointer + FRAME_LENGTH]

        comp = np.correlate(frame, rr, "full")
        maxp = np.argmax(np.abs(comp))
        if comp[maxp] >= 0:
            detected_bit[i] = 1
        else:
            detected_bit[i] = 0

        pointer = pointer + frame_shift

    if REP_CODE:
        count = 0
        wmark_recovered = np.zeros(effective_nbit)

        for i in range(effective_nbit):
            ave = np.sum(detected_bit[count:count+NUM_REPS]) / NUM_REPS

            if ave >= 0.5:
                wmark_recovered[i] = 1
            else:
                wmark_recovered[i] = 0

            count = count + NUM_REPS
    else:
        wmark_recovered = detected_bit

    # ビット誤り率を表示
    BER = np.sum(np.abs(wmark_recovered - wmark_original)) / \
        effective_nbit * 100
    print(f'bit error rate = {BER} %')

    # SNRを表示
    SNR = 10 * np.log10(
        np.sum(np.square(host_signal.astype(np.float32)))
        / np.sum(np.square(host_signal.astype(np.float32)
                           - eval_signal.astype(np.float32))))
    print(f'SNR = {SNR}dB')


def main():
    """Main routine. """

    embed()                     # 透かしの埋め込み
    detect()                    # 透かしの検出


if __name__ in '__main__':
    main()
