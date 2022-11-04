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
# gTTSによるテキスト音声合成のサンプルスクリプト with PySimpleGUI

import subprocess

import PySimpleGUI as sg
from gtts import gTTS

# 一時用保存ファイル
OUT_MP3 = "/tmp/tts.mp3"

# 合成エンジンの言語
LANG = "ja"

# フォント指定
FONT = ("Hiragino Maru Gothic ProN", 24)

# レイアウト定義
LAYOUT = [
    [
        sg.InputText("音声合成のサンプルです", size=(35, 1), key="txt"),
    ],
    [
        sg.Button("合成", key="synth"),
        sg.Button("終了", key="quit"),
    ],
]

# ウィンドウ生成
WINDOW = sg.Window("TTS-sample", LAYOUT, font=FONT)

# イベントループ
while True:

    # イベント読み込み
    event, values = WINDOW.read()

    if event == sg.WINDOW_CLOSED or event == "quit":
        break

    elif event == "synth":  # 入力されたテキストを音声合成する
        text = values["txt"]

        # 音声合成（テキストデータ→音声データ）
        tts = gTTS(text, lang=LANG)

        # mp3形式でファイルを保存
        tts.save(OUT_MP3)

        # 再生
        subprocess.run("afplay " + OUT_MP3, shell=True)

# ウィンドウを閉じて終了
WINDOW.close()
