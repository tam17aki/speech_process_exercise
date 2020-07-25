#!/usr/bin/env python3

"""A python script to perform watermark embedding/detection
   on the basis of singular value decomposition (SVD) method."""

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
    # STFT行列を特異値分解
    U, D, V = np.linalg.svd(stft_mat, full_matrices=False)

    off_diag_index = np.where(~np.eye(np.diag(D).shape[0], dtype=bool))
    embed_nbit = len(off_diag_index[0])
    if REP_CODE:
        # 実効的な埋め込み可能ビット数
        effective_nbit = int(np.floor(embed_nbit / NUM_REPS))

        embed_nbit = int(effective_nbit * NUM_REPS)
    else:
        effective_nbit = embed_nbit

    # オリジナルの透かし信号を作成（0と1のビット列）
    wmark_original = np.random.randint(2, size=effective_nbit)

    # オリジナルの透かし信号を保存
    with open(WATERMARK_ORIGINAL_FILE, 'wb') as f:
        pickle.dump(wmark_original, f)

    wmark_original = 2 * wmark_original - 1  # 1と-1に変換する

    # 透かし信号を拡張する
    if REP_CODE:
        wmark_extended = np.repeat(wmark_original, NUM_REPS)
    else:
        wmark_extended = wmark_original

    # 埋め込み強度
    alpha = CONTROL_STRENGTH

    # 透かしの埋め込み
    wmed_D = np.diag(D)
    embed = alpha * wmark_extended
    row_index = off_diag_index[0]
    col_index = off_diag_index[1]
    for i in range(embed_nbit):
        wmed_D[row_index[i], col_index[i]] = embed[i]

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

    # オリジナルの透かし信号をロード
    with open(WATERMARK_ORIGINAL_FILE, 'rb') as f:
        wmark_original = pickle.load(f)

    # STFT行列を特異値分解
    U, Dw, V = np.linalg.svd(wmed_stft_mat, full_matrices=False)

    off_diag_index = np.where(~np.eye(np.diag(D).shape[0], dtype=bool))
    embed_nbit = len(off_diag_index[0])
    if REP_CODE:
        # 実効的な埋め込み可能ビット数
        effective_nbit = int(np.floor(embed_nbit / NUM_REPS))

        embed_nbit = int(effective_nbit * NUM_REPS)
    else:
        effective_nbit = embed_nbit

    # 透かし入りの行列を再構築
    wmed_D = Uw @ np.diag(Dw) @ Vw

    # 埋め込み強度
    alpha = CONTROL_STRENGTH

    # 対角成分を除去し、「拡張透かし」を復元
    W = (wmed_D - np.diag(D))
    W = (1.0 / alpha) * W

    # 残りの対角成分を正規化
    W_diag = W.diagonal() / np.abs(D)
    W = W - np.diag(W.diagonal())
    W = W + np.diag(W_diag)

    # ビットに変換
    detected_bit = np.zeros((embed_nbit))
    row_index = off_diag_index[0]
    col_index = off_diag_index[1]
    for i in range(embed_nbit):
        if W[row_index[i], col_index[i]] > THRESHOLD:
            detected_bit[i] = 1

    # 「透かし」を復元
    wmark_recovered = np.zeros((effective_nbit))
    count = 0
    for i in range(effective_nbit):
        # ビットを集計（平均値）
        ave = np.sum(detected_bit[count:count + NUM_REPS]) / NUM_REPS

        if ave >= 0.5:      # 過半数
            wmark_recovered[i] = 1
        else:
            wmark_recovered[i] = 0

        count = count + NUM_REPS

    # ビット誤り率を表示
    denom = np.int(np.sum(np.abs(wmark_recovered - wmark_original)))
    BER = np.sum(np.abs(wmark_recovered - wmark_original)) / \
        (effective_nbit) * 100
    print(f'bit error rate = {BER:.2f}% ({denom} / {effective_nbit})')

    # SNRを表示
    SNR = 10 * np.log10(
        np.sum(np.square(host_signal.astype(np.float32)))
        / np.sum(np.square(host_signal.astype(np.float32)
                           - eval_signal.astype(np.float32))))
    print(f'SNR = {SNR}dB')

    # bpsを表示
    print('BPS = {:.2f} bps'.format(
        effective_nbit / (len(host_signal) / sr)))


def main():
    """Main routine. """
    embed()
    detect()


if __name__ in '__main__':
    main()
