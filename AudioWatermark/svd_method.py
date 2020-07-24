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
import librosa
import pickle


HOST_SIGNAL_FILE = "host.wav"  # 透かし埋め込み先のファイル
WATERMARK_SIGNAL_FILE = "wmed_signal.wav"           # 透かしを埋め込んだファイル
WATERMARK_U_FILE = 'svd_left.dat'                 # 特異値分解の左側の行列
WATERMARK_D_FILE = 'svd_center.dat'                 # 特異値分解の真ん中の行列
WATERMARK_V_FILE = 'svd_right.dat'                # 特異値分解の右側の行列
WATERMARK_ORIGINAL_FILE = 'watermark_ori.dat'       # オリジナルの透かし信号

REP_CODE = True                 # 繰り返し埋め込みを使う
FRAME_LENGTH = 2048             # フレーム長
FFT_LENGTH = FRAME_LENGTH
HOP_LENGTH = 80

CONTROL_STRENGTH = 0.01         # 埋め込み強度
NUM_REPS = 3                    # 埋め込みの繰り返し数
THRESHOLD = 0.0


def embed():
    """
    perform embedding.
    """

    sr, host_signal = wavfile.read(HOST_SIGNAL_FILE)
    host_signal = host_signal.astype(np.float64)
    signal_len = len(host_signal)

    # STFT行列を作成
    stft_mat = librosa.core.stft(host_signal, n_fft=FFT_LENGTH,
                                 hop_length=HOP_LENGTH).T
    n_frames = stft_mat.shape[0]

    # STFT行列を特異値分解
    U, D, V = np.linalg.svd(stft_mat, full_matrices=False)

    # 埋め込みの総ビット数
    embed_nbit = n_frames

    if REP_CODE:
        # 実効的な埋め込み可能ビット数
        effective_nbit = np.floor(embed_nbit / NUM_REPS)

        embed_nbit = effective_nbit * NUM_REPS
    else:
        effective_nbit = embed_nbit

    # 整数化
    effective_nbit = int(effective_nbit)
    embed_nbit = int(embed_nbit)

    # オリジナルの透かし信号を作成（0と1のビット列）
    wmark_original = np.random.randint(2, size=(effective_nbit, effective_nbit))
    # オリジナルの透かし信号を保存
    with open(WATERMARK_ORIGINAL_FILE, 'wb') as f:
        pickle.dump(wmark_original, f)

    wmark_original = 2 * wmark_original - 1  # 1と-1に変換する

    # 透かし信号を拡張する
    if REP_CODE:
        wmark_extended = np.repeat(wmark_original, NUM_REPS, axis=0)
        wmark_extended = np.repeat(wmark_extended, NUM_REPS, axis=1)
    else:
        wmark_extended = wmark_original

    # 埋め込み強度
    alpha = CONTROL_STRENGTH

    # 透かしの埋め込み
    rows = wmark_extended.shape[0]
    cols = wmark_extended.shape[1]
    wmed_D = np.diag(D)
    wmed_D[:rows, :cols] = wmed_D[:rows, :cols] + alpha * wmark_extended

    # 埋め込んだ行列を特異値分解
    Uw, Dw, Vw = np.linalg.svd(wmed_D, full_matrices=False)

    # 行列を保存する
    with open(WATERMARK_U_FILE, 'wb') as f:
        pickle.dump(Uw, f)
    with open(WATERMARK_D_FILE, 'wb') as f:
        pickle.dump(D, f)
    with open(WATERMARK_V_FILE, 'wb') as f:
        pickle.dump(Vw, f)

    # 再構築
    wmed_stft_mat = U @ np.diag(Dw) @ V
    wmed_stft_mat = wmed_stft_mat.T

    # inverse STFTで逆変換
    wmed_signal = librosa.core.istft(wmed_stft_mat, hop_length=HOP_LENGTH)
    wmed_signal = np.concatenate(
        (wmed_signal, host_signal[len(wmed_signal): signal_len]))

    # 透かしが埋め込まれた信号をwavとして保存
    wmed_signal = wmed_signal.astype(np.int16)  # convert float into integer
    wavfile.write(WATERMARK_SIGNAL_FILE, sr, wmed_signal)


def detect():
    """
    perform detecton.
    """

    # ホスト信号のロード
    sr, host_signal = wavfile.read(HOST_SIGNAL_FILE)

    # 埋め込み済みの音声ファイルを開く
    _, eval_signal = wavfile.read(WATERMARK_SIGNAL_FILE)
    eval_signal = eval_signal.astype(np.float64)

    # 透かしの埋め込みに用いた行列をロードする
    with open(WATERMARK_U_FILE, 'rb') as f:
        Uw = pickle.load(f)
    with open(WATERMARK_D_FILE, 'rb') as f:
        D = pickle.load(f)
    with open(WATERMARK_V_FILE, 'rb') as f:
        Vw = pickle.load(f)

    # STFT行列を作成
    wmed_stft_mat = librosa.core.stft(eval_signal, n_fft=FFT_LENGTH,
                                      hop_length=HOP_LENGTH).T

    # フレーム数を確定
    n_frames = D.shape[0]
    embed_nbit = n_frames

    if REP_CODE:
        # 実質的な埋め込み可能ビット数
        effective_nbit = np.floor(embed_nbit / NUM_REPS)

        embed_nbit = effective_nbit * NUM_REPS
    else:
        effective_nbit = embed_nbit

    effective_nbit = int(effective_nbit)
    embed_nbit = int(embed_nbit)

    # オリジナルの透かし信号をロード
    with open(WATERMARK_ORIGINAL_FILE, 'rb') as f:
        wmark_original = pickle.load(f)

    # STFT行列を特異値分解
    U, Dw, V = np.linalg.svd(wmed_stft_mat, full_matrices=False)

    # 透かし入りの行列を再構築
    wmed_D = Uw @ np.diag(Dw) @ Vw

    # 埋め込み強度
    alpha = CONTROL_STRENGTH

    # 対角成分を除去し、「拡張透かし」を復元
    W = (wmed_D - np.diag(D))
    W = (1.0 / alpha) * W

    # 残りの対角成分を正規化
    W_diag = W.diagonal() / D
    W = W - np.diag(W.diagonal())
    W = W + np.diag(W_diag)

    # 「透かし」を復元
    wmark_recovered = np.zeros((effective_nbit, effective_nbit))
    for i in range(effective_nbit):
        for j in range(effective_nbit):
            # ブロック行列の成分の和
            thres = np.sum(W[i * NUM_REPS: (i + 1) * NUM_REPS,
                             j * NUM_REPS: (j + 1) * NUM_REPS])

            if thres > THRESHOLD:
                wmark_recovered[i][j] = 1
            else:
                wmark_recovered[i][j] = 0

    # ビット誤り率を表示
    denom = np.int(np.sum(np.abs(wmark_recovered - wmark_original)))
    BER = np.sum(np.abs(wmark_recovered - wmark_original)) / \
        (effective_nbit * effective_nbit) * 100
    print(f'bit error rate = {BER:.2f}% ({denom} / {effective_nbit ** 2})')

    # SNRを表示
    SNR = 10 * np.log10(
        np.sum(np.square(host_signal.astype(np.float32)))
        / np.sum(np.square(host_signal.astype(np.float32)
                           - eval_signal.astype(np.float32))))
    print(f'SNR = {SNR}dB')

    # bpsを表示
    print('BPS = {:.2f} bps'.format(
        effective_nbit ** 2 / (len(host_signal) / sr)))


def main():
    """Main routine. """
    embed()
    detect()


if __name__ in '__main__':
    main()
