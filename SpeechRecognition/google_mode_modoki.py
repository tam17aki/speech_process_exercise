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
# Google Homeもどきを実現するサンプル

import PySimpleGUI as sg
import speech_recognition as sr

# マイク設定
rec = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    rec.adjust_for_ambient_noise(source)

TIMEOUT = 1000  # タイムアウト時間（単位：ミリ秒）
WAKE_WORD = "Ok Google"  # ウェイクワード

# フォント指定
FONT = ("Hiragino Maru Gothic ProN", 20)

# レイアウト定義
LAYOUT = [
    [sg.Text("お好きなタイミングで話しかけてください", size=(35, 1))],
    [sg.Text("認識結果: ", size=(40, 1), key="-RECOG_TEXT-")],
    [sg.Button("終了", key="-QUIT-")],
]

# ウィンドウ生成
WINDOW = sg.Window("Google Home sample", LAYOUT, font=FONT)

while True:
    event, values = WINDOW.read(timeout=TIMEOUT, timeout_key="-RECOG_TRIGGER-")

    if event in (sg.WIN_CLOSED, "-QUIT-"):
        break

    elif event in "-RECOG_TRIGGER-":

        with mic as source:
            audio = rec.listen(source)
            try:  # ウェイクワードの認識
                text = rec.recognize_google(audio, language="ja-JP")
                if WAKE_WORD in text:  # 認識結果にウェイクワードが含まれるならば

                    # 認識結果文字列のWAKE_WORDを空文字列で置き換える
                    # →後段の処理に利用可能
                    text = text.replace(WAKE_WORD, "")

                    WINDOW["-RECOG_TEXT-"].Update("認識結果: " + text)
                else:
                    # 認識結果をクリア
                    WINDOW["-RECOG_TEXT-"].Update("認識結果: ")

            except sr.UnknownValueError:
                WINDOW["-RECOG_TEXT-"].Update("認識に失敗しました")

WINDOW.close()
