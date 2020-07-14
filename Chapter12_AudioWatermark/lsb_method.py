#!/usr/bin/env python3

""" A python script to perform audio watermark embedding/detection
    on the basis of least significant bit (LSB) modification method."""

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

REP_CODE = True                 # 繰り返し埋め込みを使う
NUM_REPS = 3                    # 埋め込みの繰り返し数
NUM_LSB = 1


def embed():
    """
    perform embedding.
    """

    # ホスト信号をロード
    sr, host_signal = wavfile.read(HOST_SIGNAL_FILE)
    signal_len = len(host_signal)

    # 埋め込みの総ビット数
    embed_nbit = signal_len

    if REP_CODE:
        # 実効的な埋め込み可能ビット数
        effective_nbit = int(np.floor(embed_nbit / NUM_REPS))

        embed_nbit = effective_nbit * NUM_REPS
    else:
        effective_nbit = embed_nbit

    # オリジナルの透かし信号を作成（0と1のビット列）
    wmark_original = np.random.randint(2, size=int(effective_nbit))

    # オリジナルの透かし信号を保存
    with open(WATERMARK_ORIGINAL_FILE, 'w') as f:
        for d in wmark_original:
            f.write("%d\n" % d)

    # 透かし信号を拡張する
    if REP_CODE:
        wmark_bits = np.repeat(wmark_original, NUM_REPS)
    else:
        wmark_bits = wmark_original

    # 埋め込み可能bit数 (NUM_LSM が 2以上の場合に意味あり)
    bit_height = int(np.ceil(embed_nbit / NUM_LSB))
    wmark_bits.resize(bit_height * NUM_LSB)

    # 量子化bit数をバイト数に変換 (ex. 16 bit -> 2 byte)
    byte_depth = host_signal.dtype.itemsize

    # 入力音声を1バイトごとに切り分けて2進数列化
    host_bits = np.unpackbits(host_signal.view(np.uint8))

    # 2進数列を (時間長, 16bit)の2進配列化
    host_bits = host_bits.reshape(signal_len, 8 * byte_depth)

    # ホスト信号のLSBを透かしで置き換える
    wmark_bits = wmark_bits.reshape(bit_height, NUM_LSB)
    host_bits[:bit_height, 8 - NUM_LSB: 8] = wmark_bits

    # ビット配列の8要素(1バイト)ごとに10進数(uint8)配列に戻す
    host_uint = np.packbits(host_bits)

    # uint8 を 16bitごとにまとめて short int の配列に戻す
    wmed_signal = np.frombuffer(host_uint, dtype=np.int16, count=-1)

    # 透かしが埋め込まれた信号をwavとして保存
    wavfile.write(WATERMARK_SIGNAL_FILE, sr, wmed_signal)


def detect():
    """
    perform detecton.
    """

    # ホスト信号をロード
    sr, host_signal = wavfile.read(HOST_SIGNAL_FILE)

    # 埋め込み済みの音声ファイルを開く
    _, wmed_signal = wavfile.read(WATERMARK_SIGNAL_FILE)
    signal_len = len(wmed_signal)

    # オリジナルの透かし信号をロード
    with open(WATERMARK_ORIGINAL_FILE, 'r') as f:
        wmark_original = f.readlines()
    wmark_original = np.array([float(w.rstrip()) for w in wmark_original])

    # 埋め込みの総ビット数
    embed_nbit = signal_len

    if REP_CODE:
        # 実効的な埋め込み可能ビット数
        effective_nbit = int(np.floor(embed_nbit / NUM_REPS))
    else:
        effective_nbit = embed_nbit

    # 埋め込み可能ビット数 (NUM_LSM が 2以上の場合に意味あり)
    bit_height = int(np.ceil(embed_nbit / NUM_LSB))

    # オリジナルの透かし信号をロード
    with open(WATERMARK_ORIGINAL_FILE, 'r') as f:
        wmark_original = f.readlines()
    wmark_original = np.array([int(w.rstrip()) for w in wmark_original])

    # 量子化bit数をバイト数に変換 (ex. 16 bit -> 2 byte)
    byte_depth = wmed_signal.dtype.itemsize

    # 透かし入り音声を1バイトごとに切り分けて2進数列化
    wmed_bits = np.unpackbits(wmed_signal.view(np.uint8))

    # 2進数列を (時間長, 16bit)の2進配列化
    wmed_bits = wmed_bits.reshape(signal_len, 8 * byte_depth)

    # 透かし情報の検出
    detected_bits = wmed_bits[:bit_height, 8 - NUM_LSB: 8]
    if REP_CODE:
        count = 0
        wmark_recovered = np.zeros(effective_nbit)

        for i in range(effective_nbit):

            # ビットを集計（平均値）
            ave = np.sum(detected_bits[count:count + NUM_REPS]) / NUM_REPS

            if ave >= 0.5:      # 過半数
                wmark_recovered[i] = 1
            else:
                wmark_recovered[i] = 0

            count = count + NUM_REPS
    else:
        wmark_recovered = detected_bits

    # ビット誤り率を表示
    denom = np.int(np.sum(np.abs(wmark_recovered - wmark_original)))
    BER = np.sum(np.abs(wmark_recovered - wmark_original)) / \
        effective_nbit * 100
    print(f'BER = {BER} % ({denom} / {effective_nbit})')

    # SNRを表示
    SNR = 10 * np.log10(
        np.sum(np.square(host_signal.astype(np.float32)))
        / np.sum(np.square(host_signal.astype(np.float32)
                           - wmed_signal.astype(np.float32))))
    print(f'SNR = {SNR:.2f} dB')

    # bpsを表示
    print('BPS = {:.2f} bps'.format(effective_nbit / (len(host_signal) / sr)))


def main():
    """Main routine. """

    embed()  # 透かしの埋め込み
    detect()  # 透かしの検出


if __name__ in '__main__':
    main()
