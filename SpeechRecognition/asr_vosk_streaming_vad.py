# -*- coding: utf-8 -*-
"""マイク音声入力によるストリーミング音声認識（発話区間検出付き）via VOSK.

Copyright (C) 2022 by Akira TAMAMORI
Copyright (C) 2022 by Koji INOUE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
import math
import queue
import struct
import sys
from collections import namedtuple
from typing import NamedTuple

import numpy as np
import sounddevice as sd
from vosk import KaldiRecognizer, Model, SetLogLevel


class VadConfig(NamedTuple):
    """発話区間検出を設定するクラス.

    threshold (int): 発話区間検出を判定するパワーのしきい値 (dB)
    vad_start (float): 発話区間を開始判定する秒数（sec）
    vad_end (float): 発話区間を終了判定する秒数 (sec)
    """

    threshold: int = 45
    vad_start: float = 0.3
    vad_end: float = 1.0


class MicrophoneStream:
    """マイク音声入力のためのクラス."""

    def __init__(self, rate, chunk, vad_config):
        """音声入力ストリームを初期化する.

        Args:
           rate (int): サンプリングレート (Hz)
           chunk (int): 音声データを受け取る単位（サンプル数）
           vad_config (VadConfig): 発話区間検出の設定
        """
        # マイク入力のパラメータ
        self.rate = rate
        self.chunk = chunk

        # 入力された音声データを保持するデータキュー（バッファ）
        self.buff = queue.Queue()

        # 発話区間検出のパラメータ
        self.vad_config = {
            "threshold": vad_config.threshold,
            "vad_start": vad_config.vad_start,
            "vad_end": vad_config.vad_end,
        }

        # 発話区間検出の作業用変数
        self.workspace = {
            "is_speaking": False,  # 現在発話区間を認定しているか
            "count_on": 0,  # 現在まででしきい値以上の区間が連続している数
            "count_off": 0,  # 現在まででしきい値以下の区間が連続している数
            "voice_end": False,  # 発話が終了したか
            "str_current_power": "",  # 現在のパワーの値を確認するための文字列（音声認識のクラスから参照）
        }

        # マイク音声入力の初期化
        self.input_stream = None

    def open_stream(self):
        """マイク音声入力の開始"""
        self.input_stream = sd.RawInputStream(
            samplerate=self.rate,
            blocksize=self.chunk,
            dtype="int16",
            channels=1,
            callback=self.callback,
        )

    def callback(self, indata, frames, time, status):
        """音声入力の度に呼び出される関数.
        音声パワーに基づいて発話区間を判定.
        """
        if status:
            print(status, file=sys.stderr)

        # 入力された音声データをキューへ保存
        self.buff.put(bytes(indata))

        # 音声のパワー（音声データの二乗平均）を計算する
        indata2 = struct.unpack(f"{len(indata) / 2:.0f}h", indata)
        rms = math.sqrt(np.square(indata2).mean())
        power = 20 * math.log10(rms) if rms > 0.0 else -math.inf  # RMSからデシベルへ

        self.workspace["str_current_power"] = f"音声パワー {power:5.1f}[dB] "
        print("\r" + self.workspace["str_current_power"], end="")

        # 音声パワーがしきい値以上、かつ発話区間をまだ認定していない場合
        if (
            power >= self.vad_config["threshold"]
            and self.workspace["is_speaking"] is False
        ):

            # しきい値以上の区間のカウンタを増やす
            self.workspace["count_on"] += 1

            # しきい値以上の区間の長さを秒単位に変換
            count_on_sec = float(self.workspace["count_on"] * self.chunk) / self.rate

            # 発話区間の開始を認定するしきい値と比較
            if count_on_sec >= self.vad_config["vad_start"]:
                self.workspace["is_speaking"] = True
                self.workspace["count_on"] = 0

        if power < self.vad_config["threshold"] and self.workspace["is_speaking"]:

            # しきい値以下の区間のカウンタを増やす
            self.workspace["count_off"] += 1

            # しきい値以下の区間の長さを秒単位に変換
            count_off_sec = float(self.workspace["count_off"] * self.chunk) / self.rate

            # 発話区間の終了を認定するしきい値と比較
            if count_off_sec >= self.vad_config["vad_end"]:
                self.workspace["voice_end"] = True
                self.workspace["count_off"] = 0

            # しきい値と比較して、反対の条件のカウンタをリセット
            if power >= self.vad_config["threshold"]:
                self.workspace["count_off"] = 0
            else:
                self.workspace["count_on"] = 0

    def generator(self):
        """音声認識に必要な音声データを取得するための関数."""
        while True:  # キューに保存されているデータを全て取り出す
            # 先頭のデータを取得
            chunk = self.buff.get()
            if chunk is None:
                return
            data = [chunk]

            # まだキューにデータが残っていれば全て取得する
            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            # yieldにすることでキューのデータを随時取得できるようにする
            yield b"".join(data)


def get_asr_result(vosk_asr):
    """音声認識APIを実行して最終的な認識結果を得る.

    Args:
       vosk_asr (VoskStreamingASR): 音声認識モジュール

    Returns:
       recog_text (str): 音声認識結果
    """
    mic_stream = vosk_asr.microphone_stream
    mic_stream.open_stream()
    with mic_stream.input_stream:
        audio_generator = mic_stream.generator()
        for content in audio_generator:
            if vosk_asr.recognizer.AcceptWaveform(content):
                recog_result = json.loads(vosk_asr.recognizer.Result())
                recog_text = recog_result["text"].split()
                recog_text = "".join(recog_text)  # 空白記号を除去
                return recog_text
        return None


def main(chunk_size=8000, threshold=45, vad_start=0.3, vad_end=1.0):
    """音声認識デモンストレーションを実行.

    Args:
       chunk_size (int): 音声データを受け取る単位（サンプル数）
       threshold (int): 発話区間検出を判定するパワーのしきい値 (dB)
       vad_start (float): 発話区間を開始判定する秒数（sec）
       vad_end (float): 発話区間を終了判定する秒数 (sec)
    """
    SetLogLevel(-1)  # VOSK起動時のログ表示を抑制

    # 入力デバイス情報に基づき、サンプリング周波数の情報を取得
    input_device_info = sd.query_devices(kind="input")
    sample_rate = int(input_device_info["default_samplerate"])

    # 発話区間検出の設定
    vad_config = VadConfig(threshold, vad_start, vad_end)

    # マイク入力を初期化・開始
    mic_stream = MicrophoneStream(sample_rate, chunk_size, vad_config)

    # 音声認識器を構築
    recognizer = KaldiRecognizer(Model("model"), sample_rate)

    # マイク入力ストリームおよび音声認識器をまとめて保持
    VoskStreamingASR = namedtuple(
        "VoskStreamingASR", ["microphone_stream", "recognizer"]
    )
    vosk_asr = VoskStreamingASR(mic_stream, recognizer)

    print("＜認識開始＞")
    recog_result = get_asr_result(vosk_asr)
    print(f"認識結果: {recog_result}")
    print("＜認識終了＞")


if __name__ == "__main__":
    main()
