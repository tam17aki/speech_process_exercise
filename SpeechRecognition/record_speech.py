#!/usr/bin/env python3

""" 音声情報処理 n本ノック !! """

# MIT License

# Copyright (C) 2022 by Akira TAMAMORI

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
# 指定秒数だけ音声を録音

from typing import NamedTuple
import sounddevice as sd  # 録音・再生系のライブラリ
import soundfile as sf  # 読み込み・書き出しのライブラリ


class RecordingConfig(NamedTuple):
    """Configuration for recording."""

    sample_rate: float = 16000  # Hz
    duration: int = 3.0  # sec
    n_channels: int = 1  # 1: mono


def record_wav(out_wavfile: str, config: RecordingConfig):
    """音声(wav)を録音する.

    Args:
        out_wavfile (str): 出力となるwavファイル名
        config (RecordingConfig): 録音の設定
    """
    sample_rate = config.sample_rate
    duration = config.duration
    n_channels = config.n_channels

    # 音声録音を指定秒数実行
    audio = sd.rec(
        int(duration * sample_rate), samplerate=sample_rate, channels=n_channels
    )
    sd.wait()

    # ファイルに書き込む
    sf.write(
        file=out_wavfile,
        data=audio,
        samplerate=sample_rate,
        format="WAV",
        subtype="PCM_16",
    )


def main(duration: int = 3.0, wav_file: str = "out.wav"):
    """音声を録音する.

    Args:
        duration (int): 録音秒数
        wav_file (str): 出力wavファイルへのパス
    """
    # 入力デバイス情報に基づき、サンプリング周波数の情報を取得
    input_device_info = sd.query_devices(kind="input")
    sample_rate = int(input_device_info["default_samplerate"])

    # 指定秒数だけ音声を録音
    record_config = RecordingConfig(sample_rate, duration)
    print("＜録音開始＞")
    record_wav(wav_file, record_config)
    print("＜認識終了＞")


if __name__ == "__main__":
    main()
