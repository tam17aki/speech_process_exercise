#!/usr/bin/env python3

"""A python script to perform watermark embedding/detection
   on the basis of echo hiding method."""

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
from scipy.signal import windows

HOST_SIGNAL_FILE = "bass_half.wav"  # 透かし埋め込み先のファイル
WATERMARK_SIGNAL_FILE1 = "wmed_signal1.wav"  # 透かしを埋め込んだファイル
WATERMARK_SIGNAL_FILE2 = "wmed_signal2.wav"  # 透かしを埋め込んだファイル
WATERMARK_SIGNAL_FILE3 = "wmed_signal3.wav"  # 透かしを埋め込んだファイル

PSEUDO_RAND_FILE = 'pseudo_rand.dat'                # 疑似乱数列のファイル
WATERMARK_ORIGINAL_FILE = 'watermark_ori.dat'       # オリジナルの透かし信号
WATERMARK_EXTENDED_FILE = 'watermark_extended.dat'  # 拡張透かし信号
SECRET_KEY_FILE = 'secret_key.dat'  # 秘密鍵（疑似乱数）

REP_CODE = True                 # 繰り返し埋め込みを使う
FRAME_LENGTH = 4096             # フレーム長
CONTROL_STRENGTH = 0.2          # 埋め込み強度
OVERLAP = 0.5                   # フレーム分析のオーバーラップ率 (固定)
NUM_REPS = 3                    # 埋め込みの繰り返し数

NEGATIVE_DELAY = 4

LOG_FLOOR = 0.00001


def fix(xs):
    """
    A emuration of MATLAB 'fix' function.
    borrowed from https://ideone.com/YjJwOh
    """

    # res = [np.floor(e) if e >= 0 else np.ceil(e) for e in xs]
    if xs >= 0:
        res = np.floor(xs)
    else:
        res = np.ceil(xs)

    return res


def embed():
    """
    perform embedding.
    """

    sr, host_signal = wavfile.read(HOST_SIGNAL_FILE)
    signal_len = len(host_signal)

    # フレームの移動量
    frame_shift = int(FRAME_LENGTH * (1 - OVERLAP))

    # 隣接フレームとのオーバーラップ長
    overlap_length = int(FRAME_LENGTH * OVERLAP)

    # 埋め込みの総ビット数
    embed_nbit = fix((signal_len - overlap_length) / frame_shift)

    if REP_CODE:
        # 実効的な埋め込み可能ビット数
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

    # 秘密鍵を作成（疑似乱数）
    secret_key = np.random.randint(2, size=int(effective_nbit))

    # 秘密鍵を拡張する
    if REP_CODE:
        secret_key_extended = np.repeat(secret_key, NUM_REPS)
    else:
        secret_key_extended = secret_key

    # 秘密鍵を保存する
    with open(SECRET_KEY_FILE, 'w') as f:
        for d in np.squeeze(secret_key_extended):
            f.write("%f\n" % d)

    # エコーカーネル
    # for key 1
    delay11 = 100
    delay10 = 110
    # for key 0
    delay01 = 120
    delay00 = 130

    # ###### エコーハイディングによる透かし埋め込み ######
    pointer = 0

    echoed_signal1 = np.zeros((frame_shift * embed_nbit))  # watermarked signal
    echoed_signal2 = np.zeros((frame_shift * embed_nbit))  # watermarked signal
    echoed_signal3 = np.zeros((frame_shift * embed_nbit))  # watermarked signal

    prev1 = np.zeros((FRAME_LENGTH))
    prev2 = np.zeros((FRAME_LENGTH))
    prev3 = np.zeros((FRAME_LENGTH))

    de = NEGATIVE_DELAY  # for negative echo

    for i in range(embed_nbit):
        frame = host_signal[pointer: (pointer + FRAME_LENGTH)]

        if secret_key_extended[i] == 1:
            if wmark_extended[i] == 1:
                delay = delay11
            else:
                delay = delay10
        else:
            if wmark_extended[i] == 1:
                delay = delay01
            else:
                delay = delay00

        echo_positive = CONTROL_STRENGTH \
            * np.concatenate((np.zeros(delay),
                              frame[0:FRAME_LENGTH - delay]))

        echo_negative = - CONTROL_STRENGTH \
            * np.concatenate((np.zeros(delay + de),
                              frame[0:FRAME_LENGTH - delay - de]))

        echo_forward = CONTROL_STRENGTH \
            * np.concatenate((frame[delay:FRAME_LENGTH], np.zeros(delay)))

        echoed_frame1 = frame + echo_positive
        echoed_frame2 = frame + echo_positive + echo_negative
        echoed_frame3 = frame + echo_positive + echo_forward

        echoed_frame1 = echoed_frame1 * windows.hann(FRAME_LENGTH)
        echoed_signal1[frame_shift * i: frame_shift * (i+1)] = \
            np.concatenate((prev1[frame_shift:FRAME_LENGTH] +
                            echoed_frame1[0:overlap_length],
                            echoed_frame1[overlap_length:frame_shift]))
        prev1 = echoed_frame1

        echoed_frame2 = echoed_frame2 * windows.hann(FRAME_LENGTH)
        echoed_signal2[frame_shift * i: frame_shift * (i+1)] = \
            np.concatenate((prev2[frame_shift: FRAME_LENGTH] +
                            echoed_frame2[0:overlap_length],
                            echoed_frame2[overlap_length:frame_shift]))
        prev2 = echoed_frame2

        echoed_frame3 = echoed_frame3 * windows.hann(FRAME_LENGTH)
        echoed_signal3[frame_shift * i: frame_shift * (i+1)] = \
            np.concatenate((prev3[frame_shift:FRAME_LENGTH] +
                            echoed_frame3[0:overlap_length],
                            echoed_frame3[overlap_length:frame_shift]))
        prev3 = echoed_frame3

        pointer = pointer + frame_shift

    echoed_signal1 = np.concatenate(
        (echoed_signal1, host_signal[len(echoed_signal1): signal_len]))

    echoed_signal2 = np.concatenate(
        (echoed_signal2, host_signal[len(echoed_signal2): signal_len]))

    echoed_signal3 = np.concatenate(
        (echoed_signal3, host_signal[len(echoed_signal3): signal_len]))

    # 透かしが埋め込まれた信号をwavとして保存
    echoed_signal1 = echoed_signal1.astype(np.int16)
    wavfile.write(WATERMARK_SIGNAL_FILE1, sr, echoed_signal1)

    echoed_signal2 = echoed_signal2.astype(np.int16)
    wavfile.write(WATERMARK_SIGNAL_FILE2, sr, echoed_signal2)

    echoed_signal3 = echoed_signal3.astype(np.int16)
    wavfile.write(WATERMARK_SIGNAL_FILE3, sr, echoed_signal3)


def detect():
    """
    perform detecton.
    """

    sr, host_signal = wavfile.read(HOST_SIGNAL_FILE)

    # 埋め込み済みの音声ファイルを開く
    _, eval_signal1 = wavfile.read(WATERMARK_SIGNAL_FILE1)
    _, eval_signal2 = wavfile.read(WATERMARK_SIGNAL_FILE2)
    _, eval_signal3 = wavfile.read(WATERMARK_SIGNAL_FILE3)
    signal_len = len(eval_signal1)

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

    # 秘密鍵をロード
    with open(SECRET_KEY_FILE, 'r') as f:
        secret_key = f.readlines()
    secret_key = np.array([float(w.rstrip()) for w in secret_key])

    # エコーカーネル
    # key 1
    delay11 = 100
    delay10 = 110
    # key 0
    delay01 = 120
    delay00 = 130

    # 検出
    pointer = 0
    detected_bit1 = np.zeros(embed_nbit)
    detected_bit2 = np.zeros(embed_nbit)
    detected_bit3 = np.zeros(embed_nbit)
    for i in range(embed_nbit):
        wmarked_frame1 = eval_signal1[pointer: pointer + FRAME_LENGTH]
        ceps1 = np.fft.ifft(
            np.log(np.square(np.fft.fft(wmarked_frame1)) + LOG_FLOOR)).real
        # print(ceps1)

        wmarked_frame2 = eval_signal2[pointer: pointer + FRAME_LENGTH]
        ceps2 = np.fft.ifft(
            np.log(np.square(np.fft.fft(wmarked_frame2)) + LOG_FLOOR)).real

        wmarked_frame3 = eval_signal3[pointer: pointer + FRAME_LENGTH]
        ceps3 = np.fft.ifft(
            np.log(np.square(np.fft.fft(wmarked_frame3)) + LOG_FLOOR)).real

        if secret_key[i] == 1:
            if ceps1[delay11] > ceps1[delay10]:
                detected_bit1[i] = 1
            else:
                detected_bit1[i] = 0

            if (ceps2[delay11] - ceps2[delay11 + NEGATIVE_DELAY]) > \
               (ceps2[delay10] - ceps2[delay10 + NEGATIVE_DELAY]):
                detected_bit2[i] = 1
            else:
                detected_bit2[i] = 0

            if ceps3[delay11] > ceps3[delay10]:
                detected_bit3[i] = 1
            else:
                detected_bit3[i] = 0

        else:
            if ceps1[delay01] > ceps1[delay00]:
                detected_bit1[i] = 1
            else:
                detected_bit1[i] = 0

            if (ceps2[delay01] - ceps2[delay01 + NEGATIVE_DELAY]) > \
               (ceps2[delay00] - ceps2[delay00 + NEGATIVE_DELAY]):
                detected_bit2[i] = 1
            else:
                detected_bit2[i] = 0

            if ceps3[delay01] > ceps3[delay00]:
                detected_bit3[i] = 1
            else:
                detected_bit3[i] = 0

        pointer = pointer + frame_shift

    if REP_CODE:
        count = 0
        wmark_recovered1 = np.zeros(effective_nbit)
        wmark_recovered2 = np.zeros(effective_nbit)
        wmark_recovered3 = np.zeros(effective_nbit)

        for i in range(effective_nbit):

            # ビットを集計（平均値）
            ave = np.sum(detected_bit1[count:count + NUM_REPS]) / NUM_REPS
            if ave >= 0.5:      # 過半数
                wmark_recovered1[i] = 1
            else:
                wmark_recovered1[i] = 0

            ave = np.sum(detected_bit2[count:count + NUM_REPS]) / NUM_REPS
            if ave >= 0.5:      # 過半数
                wmark_recovered2[i] = 1
            else:
                wmark_recovered2[i] = 0

            ave = np.sum(detected_bit3[count:count + NUM_REPS]) / NUM_REPS
            if ave >= 0.5:      # 過半数
                wmark_recovered3[i] = 1
            else:
                wmark_recovered3[i] = 0

            count = count + NUM_REPS
    else:
        wmark_recovered1 = detected_bit1
        wmark_recovered2 = detected_bit2
        wmark_recovered3 = detected_bit3

    # ビット誤り率を表示
    denom = np.int(np.sum(np.abs(wmark_recovered1 - wmark_original)))
    BER = np.sum(np.abs(wmark_recovered1 - wmark_original)) / \
        effective_nbit * 100
    print(f'bit error rate = {BER:.2f}% ({denom} / {effective_nbit})')

    denom = np.int(np.sum(np.abs(wmark_recovered2 - wmark_original)))
    BER = np.sum(np.abs(wmark_recovered2 - wmark_original)) / \
        effective_nbit * 100
    print(f'bit error rate = {BER:.2f}% ({denom} / {effective_nbit})')

    denom = np.int(np.sum(np.abs(wmark_recovered3 - wmark_original)))
    BER = np.sum(np.abs(wmark_recovered3 - wmark_original)) / \
        effective_nbit * 100
    print(f'bit error rate = {BER:.2f}% ({denom} / {effective_nbit})')

    # SNRを表示
    SNR = 10 * np.log10(
        np.sum(np.square(host_signal.astype(np.float32)))
        / np.sum(np.square(host_signal.astype(np.float32)
                           - eval_signal1.astype(np.float32))))
    print(f'SNR = {SNR:.2f} dB')
    SNR = 10 * np.log10(
        np.sum(np.square(host_signal.astype(np.float32)))
        / np.sum(np.square(host_signal.astype(np.float32)
                           - eval_signal2.astype(np.float32))))
    print(f'SNR = {SNR:.2f} dB')
    SNR = 10 * np.log10(
        np.sum(np.square(host_signal.astype(np.float32)))
        / np.sum(np.square(host_signal.astype(np.float32)
                           - eval_signal3.astype(np.float32))))
    print(f'SNR = {SNR:.2f} dB')


def main():
    """Main routine. """
    embed()
    detect()


if __name__ in '__main__':
    main()
