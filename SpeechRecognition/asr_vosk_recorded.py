# -*- coding: utf-8 -*-
"""収録済み音声ファイルに対する音声認識 via VOSK.

Copyright (C) 2022 by Akira TAMAMORI

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
import wave
import sys
import json

from vosk import Model, KaldiRecognizer, SetLogLevel


def get_asr_result(recognizer, stream, chunk_size):
    """音声認識APIを実行して最終的な認識結果を得る.

    Args:
       recognizer (KaldiRecognizer): 音声認識モジュール
       stream (Wave_read): wav読み取りのための入力ストリーム
       chunk_size (int): wavを一度に読み取るサイズ

    Returns:
       recog_text (str): 音声認識結果
    """
    while True:
        data = stream.readframes(chunk_size)
        if len(data) == 0:
            break
        recognizer.AcceptWaveform(data)

    recog_result = json.loads(recognizer.FinalResult())
    recog_text = recog_result["text"].split()
    recog_text = "".join(recog_text)
    return recog_text


def main(chunk_size=4000, wav_file="in.wav"):
    """収録済み音声に対して音声認識デモンストレーションを実行.

    Args:
       chunk_size (int): 音声データを受け取る単位（サンプル数）
       wav_file (str): wavファイルへのパス
    """
    SetLogLevel(-1)  # VOSK起動時のログ表示を抑制

    wf = wave.open(wav_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)

    model = Model("model")
    recognizer = KaldiRecognizer(model, wf.getframerate())

    recog_text = get_asr_result(recognizer, wf, chunk_size)
    print(f"認識結果: {recog_text}")


if __name__ == "__main__":
    main()
