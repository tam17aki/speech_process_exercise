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
# PyOpenJTalkによるテキスト音声合成のサンプルスクリプト

import numpy as np
import pyopenjtalk
import PySimpleGUI as sg
import sounddevice as sd

OUT_WAV = "/tmp/tts.wav"

FONT = ("Arial", 30)
LAYOUT = [
    [
        sg.InputText(default_text="音声合成のサンプルです。", size=(40, 3), key="text"),
        sg.Button("合成", key="synth"),
    ]
]

WINDOW = sg.Window("TTS-sample", LAYOUT, font=FONT)

while True:
    event, values = WINDOW.read()

    if event is None:
        break
    else:
        # 入力されたテキストを音声合成する
        if event == "synth":
            text = values["text"]

            # 音声合成（テキストデータ→音声データ）
            audio, sr = pyopenjtalk.tts(text)

            # 振幅の正規化
            audio = audio / np.abs(audio).max()
            audio = audio * (np.iinfo(np.int16).max / 2 - 1)
            audio = audio.astype(np.int16)

            # 再生
            sd.play(audio, sr)

            # 再生は非同期に行われるので、明示的にsleepさせる
            sd.sleep(int(1000 * len(audio) / sr))

WINDOW.close()
