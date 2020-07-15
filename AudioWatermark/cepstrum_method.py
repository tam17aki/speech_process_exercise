#!/usr/bin/env python3

"""A python script to perform watermark embedding/detection
   in the cepstrum domain via statistical mean manipulation."""

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
from acoustics.cepstrum import inverse_complex_cepstrum

HOST_SIGNAL_FILE = "bass_half.wav"  # 透かし埋め込み先のファイル
WATERMARK_SIGNAL_FILE = "wmed_signal.wav"           # 透かしを埋め込んだファイル
PSEUDO_RAND_FILE = 'pseudo_rand.dat'                # 疑似乱数列のファイル
WATERMARK_ORIGINAL_FILE = 'watermark_ori.dat'       # オリジナルの透かし信号
WATERMARK_EXTENDED_FILE = 'watermark_extended.dat'  # 拡張透かし信号

REP_CODE = True                 # 繰り返し埋め込みを使う
FRAME_LENGTH = 2048             # フレーム長
CONTROL_STRENGTH = 0.001        # 埋め込み強度
OVERLAP = 0.5                   # フレーム分析のオーバーラップ率 (固定)
NUM_REPS = 5                    # 埋め込みの繰り返し数
WIDTH = 5
THRESHOLD = 0.0

LOG_FLOOR = 0.00001


def complex_cepstrum(x, n=None):
    """
    Compute the complex cepstrum of a real sequence.

    http://python-acoustics.github.io/python-acoustics/_modules/acoustics/cepstrum.html
    """

    def _unwrap(phase):
        samples = phase.shape[-1]
        unwrapped = np.unwrap(phase)
        center = (samples + 1) // 2
        if samples == 1:
            center = 0
        ndelay = np.array(np.round(unwrapped[..., center] / np.pi))
        unwrapped -= np.pi * ndelay[..., None] * np.arange(samples) / center
        return unwrapped, ndelay

    spectrum = np.fft.fft(x, n=n)
    unwrapped_phase, ndelay = _unwrap(np.angle(spectrum))
    log_spectrum = np.log(np.abs(spectrum) + LOG_FLOOR) + 1j * unwrapped_phase
    ceps = np.fft.ifft(log_spectrum).real

    return ceps, ndelay


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

    alpha = CONTROL_STRENGTH

    # 透かしが埋め込まれた信号(watermarked signal)を生成 in cepstrum domain
    pointer = 0
    count = 0
    wmed_signal = np.zeros((frame_shift * embed_nbit))  # watermarked signal
    prev = np.zeros((FRAME_LENGTH))
    for i in range(embed_nbit):
        frame = host_signal[pointer: (pointer + FRAME_LENGTH)]

        # 複素ケプストラム
        real_ceps, ndelay = complex_cepstrum(frame)
        samples = len(real_ceps)

        # ケプストラム成分の「中心」の周辺に透かしをばら撒く
        center = (samples + 1) // 2
        width = FRAME_LENGTH // WIDTH
        index_range = range(center - width, center + width)

        mean_ceps = np.mean(real_ceps[index_range])
        diff_ceps = real_ceps
        diff_ceps[index_range] = real_ceps[index_range] - mean_ceps

        # 情報を埋め込む
        if wmark_extended[count] == 1:
            diff_ceps[index_range] = diff_ceps[index_range] + alpha
        else:
            diff_ceps[index_range] = diff_ceps[index_range] - alpha

        # 逆変換
        wmarked_frame = inverse_complex_cepstrum(diff_ceps, ndelay)

        # 窓をかける (Hann window)
        wmarked_frame = wmarked_frame * windows.hann(FRAME_LENGTH)

        wmed_signal[frame_shift * i: frame_shift * (i+1)] = \
            np.concatenate((prev[frame_shift:FRAME_LENGTH] +
                            wmarked_frame[0:overlap_length],
                            wmarked_frame[overlap_length:frame_shift]))

        prev = wmarked_frame
        count = count + 1
        pointer = pointer + frame_shift

    # ホスト信号の残りと結合
    wmed_signal = np.concatenate(
        (wmed_signal, host_signal[len(wmed_signal): signal_len]))

    # 透かしが埋め込まれた信号をwavとして保存
    wmed_signal = wmed_signal.astype(np.int16)  # convert float into integer
    wavfile.write(WATERMARK_SIGNAL_FILE, sr, wmed_signal)


def detect():
    """
    perform detecton.
    """

    sr, host_signal = wavfile.read(HOST_SIGNAL_FILE)

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

    pointer = 0
    thres = np.zeros(embed_nbit)
    detected_bit = np.zeros(embed_nbit)
    for i in range(embed_nbit):
        wmarked_frame = eval_signal[pointer: pointer + FRAME_LENGTH]

        # 複素ケプストラム（振幅と位相）
        wmarked_real_ceps, ndelay = complex_cepstrum(wmarked_frame)

        samples = len(wmarked_real_ceps)
        center = (samples + 1) // 2
        width = FRAME_LENGTH // WIDTH
        thres = np.sum(wmarked_real_ceps[center - width: center + width])

        # 検出
        if thres > THRESHOLD:
            detected_bit[i] = 1
        else:
            detected_bit[i] = 0

        pointer = pointer + frame_shift

    if REP_CODE:
        count = 0
        wmark_recovered = np.zeros(effective_nbit)

        for i in range(effective_nbit):

            # ビットを集計（平均値）
            ave = np.sum(detected_bit[count:count + NUM_REPS]) / NUM_REPS

            if ave >= 0.5:      # 過半数
                wmark_recovered[i] = 1
            else:
                wmark_recovered[i] = 0

            count = count + NUM_REPS
    else:
        wmark_recovered = detected_bit

    # ビット誤り率を表示
    denom = np.int(np.sum(np.abs(wmark_recovered - wmark_original)))
    BER = np.sum(np.abs(wmark_recovered - wmark_original)) / \
        effective_nbit * 100
    print(f'bit error rate = {BER}% ({denom} / {effective_nbit})')

    # SNRを表示
    SNR = 10 * np.log10(
        np.sum(np.square(host_signal.astype(np.float32)))
        / np.sum(np.square(host_signal.astype(np.float32)
                           - eval_signal.astype(np.float32))))
    print(f'SNR = {SNR}dB')


def main():
    """Main routine. """
    embed()
    detect()


if __name__ in '__main__':
    main()
