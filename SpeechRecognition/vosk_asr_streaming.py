# -*- coding: utf-8 -*-
"""マイク音声入力によるストリーミング音声認識 via VOSK.

音声情報処理 n本ノック !!

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
import queue
import sys
from collections import namedtuple

import sounddevice as sd
from vosk import KaldiRecognizer, Model, SetLogLevel


class MicrophoneStream:
    """マイク音声入力のためのクラス."""

    def __init__(self, rate, chunk):
        """音声入力ストリームを初期化する.

        Args:
           rate (int): サンプリングレート (Hz)
           chunk (int): 音声データを受け取る単位（サンプル数）
        """
        # マイク入力のパラメータ
        self.rate = rate
        self.chunk = chunk

        # 入力された音声データを保持するデータキュー（バッファ）
        self.buff = queue.Queue()

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
        """音声入力の度に呼び出される関数."""
        if status:
            print(status, file=sys.stderr)

        # 入力された音声データをキューへ保存
        self.buff.put(bytes(indata))

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


def main(chunk_size=8000):
    """音声認識デモンストレーションを実行.

    Args:
       chunk_size (int): 音声データを受け取る単位（サンプル数）
    """
    SetLogLevel(-1)  # VOSK起動時のログ表示を抑制

    # 入力デバイス情報に基づき、サンプリング周波数の情報を取得
    input_device_info = sd.query_devices(kind="input")
    sample_rate = int(input_device_info["default_samplerate"])

    # マイク入力を初期化
    mic_stream = MicrophoneStream(sample_rate, chunk_size)

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
