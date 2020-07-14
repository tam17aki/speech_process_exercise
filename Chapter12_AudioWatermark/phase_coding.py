#!/usr/bin/env python3

"""A python script to perform watermark embedding/detection
   on the basis of phase coding method."""

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
from scipy import interpolate

HOST_SIGNAL_FILE = "bass_half.wav"  # 透かし埋め込み先のファイル
WATERMARK_SIGNAL_FILE = "wmed_signal.wav"           # 透かしを埋め込んだファイル
PSEUDO_RAND_FILE = 'pseudo_rand.dat'                # 疑似乱数列のファイル
WATERMARK_ORIGINAL_FILE = 'watermark_ori.dat'       # オリジナルの透かし信号

FRAME_LENGTH = 2048             # フレーム長
HALF_FLENGTH = FRAME_LENGTH // 2
FREQ_SLOT = 64
VAD_THRES = 1.0e-3
VAD_SHIFT = 32


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
    """ Embedding. """

    sr, host_signal = wavfile.read(HOST_SIGNAL_FILE)
    signal_len = len(host_signal)

    # オリジナルの透かし信号を作成（0と1のビット列）
    watermark_len = int(HALF_FLENGTH / FREQ_SLOT)
    wmark_original = np.random.randint(2, size=int(watermark_len))

    # オリジナルの透かし信号を保存
    with open(WATERMARK_ORIGINAL_FILE, 'w') as f:
        for d in wmark_original:
            f.write("%d\n" % d)

    # サイレンスの終端位置を決定（要は簡易VAD）
    silence_point = 0
    while silence_point + FRAME_LENGTH <= signal_len:
        frame = host_signal[silence_point:
                            silence_point + FRAME_LENGTH // VAD_SHIFT]
        if np.sum(np.square(frame)) > VAD_THRES:
            break
        else:
            silence_point = silence_point + FRAME_LENGTH // VAD_SHIFT

    # STEP 1: Partition the host signal into N_seg segments,
    # each with N_frame points.
    n_segments = int(fix((signal_len - silence_point) / FRAME_LENGTH))
    pointer = silence_point
    wmed_signal = np.zeros((n_segments * FRAME_LENGTH))  # watermarked signal

    for i in range(n_segments):
        frame = host_signal[pointer: (pointer + FRAME_LENGTH)]

        # STEP 2: Calculate magnitude matrix A and phase matrix
        amplitude = np.abs(np.fft.fft(frame))

        # STEP 3: Calculate phase difference matrix
        if i == 0:
            watermark_temp = np.zeros((watermark_len + 1))

            # STEP 4: Get the initial phase vector according to the watermark
            for j in range(watermark_len):
                if wmark_original[j] == 1:
                    watermark_temp[j + 1] = np.pi / 2
                else:
                    watermark_temp[j + 1] = -np.pi / 2

            x = np.arange(watermark_len + 1)
            y = np.arange(0, watermark_len, (1.0/FREQ_SLOT))
            interp_func = interpolate.interp1d(
                x, watermark_temp, kind='cubic')
            watermark_frame = interp_func(y)
            old_phase = np.angle(np.fft.fft(frame))
            new_phase = watermark_frame
            old_pre_phase = np.zeros_like(old_phase)
            new_pre_phase = np.zeros_like(old_phase)
        else:
            old_phase = np.angle(np.fft.fft(frame))

            # phase difference between each adjacent segment
            delta_phase = old_phase - old_pre_phase
            new_phase = new_pre_phase[0: HALF_FLENGTH] + \
                delta_phase[0: HALF_FLENGTH]

        old_pre_phase = old_phase
        new_pre_phase = new_phase

        # STEP 6: Reconstruct frequency spectrum by using Euler's formula
        real_lefthalf = amplitude[0:HALF_FLENGTH] * \
            np.cos(new_phase[0:HALF_FLENGTH])

        imag_lefthalf = amplitude[0:HALF_FLENGTH] * \
            np.sin(new_phase[0:HALF_FLENGTH])

        real_righthalf = real_lefthalf[-1::-1]
        imag_righthalf = -1.0 * imag_lefthalf[-1::-1]

        # reconstruction
        freq_spec_real = np.concatenate(
            (real_lefthalf, [0], real_righthalf[:-1]))
        freq_spec_imag = np.concatenate(
            (imag_lefthalf, [0], imag_righthalf[:-1]))
        freq_frame = freq_spec_real + 1j * freq_spec_imag

        # STEP 7: IFFT back to time domain and concatenate all the frames
        reconstructed_frame = np.fft.ifft(freq_frame).real

        if i == 0:
            wmed_signal = reconstructed_frame
        else:
            wmed_signal = np.concatenate((wmed_signal, reconstructed_frame))

        pointer = pointer + FRAME_LENGTH

    wmed_signal = np.concatenate((host_signal[0:silence_point], wmed_signal))
    wmed_signal = np.concatenate((wmed_signal,
                                  host_signal[len(wmed_signal):signal_len]))

    # 透かしが埋め込まれた信号をwavとして保存
    wmed_signal = wmed_signal.astype(np.int16)  # convert float into integer
    wavfile.write(WATERMARK_SIGNAL_FILE, sr, wmed_signal)

    return silence_point


def detect(silence_point):
    """ Detection. """

    sr, host_signal = wavfile.read(HOST_SIGNAL_FILE)

    # 埋め込み済みの音声ファイルを開く
    _, eval_signal = wavfile.read(WATERMARK_SIGNAL_FILE)

    # オリジナルの透かし信号をロード
    with open(WATERMARK_ORIGINAL_FILE, 'r') as f:
        wmark_original = f.readlines()
    wmark_original = np.array([int(w.rstrip()) for w in wmark_original])

    # 無音区間をスキップした最初の有音フレーム
    first_frame = eval_signal[silence_point: FRAME_LENGTH + silence_point]

    # 位相スペクトル
    phase = np.angle(np.fft.fft(first_frame))

    # 透かし長
    watermark_len = int(HALF_FLENGTH / FREQ_SLOT)

    # 復元された透かし
    wmark_recovered = np.zeros(watermark_len + 1)

    # 透かし検出
    for i in range(watermark_len + 1):
        if phase[i * FREQ_SLOT] >= 0:
            wmark_recovered[i] = 1
        else:
            wmark_recovered[i] = 0

    # ビット誤り率(Bit Error Rate; BER)を表示
    denom = np.int(np.sum(np.abs(wmark_recovered[1:] - wmark_original)))
    BER = np.sum(np.abs(wmark_recovered[1:] - wmark_original)) / \
        watermark_len * 100
    print(f'BER = {BER}% ({denom} / {watermark_len})')

    SNR = 10 * np.log10(
        np.sum(np.square(host_signal.astype(np.float32)))
        / np.sum(np.square(host_signal.astype(np.float32)
                           - eval_signal.astype(np.float32))))
    print(f'SNR = {SNR}dB')


def main():
    """Main routine. """
    silence_point = embed()
    detect(silence_point)


if __name__ in '__main__':
    main()
