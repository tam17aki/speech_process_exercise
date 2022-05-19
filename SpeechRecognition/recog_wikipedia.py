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
# 音声認識結果に基づいてWikipediaを検索し、結果を音声合成で読み上げる（文章は最初の句点まで）

import re  # 正規表現を扱うライブラリ
import subprocess

import PySimpleGUI as sg
import sounddevice as sd  # 録音・再生系のライブラリ
import soundfile as sf  # 読み込み・書き出しのライブラリ
import speech_recognition as sr  # 音声認識のライブラリ
import wikipedia  # wikipedia検索のためのライブラリ
from gtts import gTTS  # 音声合成のライブラリ

# マイクの設定
r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)

# フォント指定
FONT = ("Hiragino Maru Gothic ProN", 20)

# 音声データ 一時保存用
AUDIO = None

SAMPLE_RATE = 16000  # サンプリング周波数
N_CHANNEL = 1  # チャンネル数 モノラルは1, ステレオは2
DURATION = 5  # 収録秒数
OUTPUT_FILE = "/tmp/record.wav"  # 出力先の音声ファイル名
OUT_MP3 = "/tmp/tts.mp3"  # 一時保存用
RECOG_TEXT = ""


# レイアウト定義
LAYOUT = [
    [sg.Text("Wikipediaで検索したい単語を音声で入力してください", size=(35, 1), key="txt")],
    [sg.Text("認識結果:", size=(40, 1), key="-RECOG_TEXT-")],
    [sg.MLine("検索結果がここに表示されます", size=(50, 5), key="wiki_result")],
    [sg.Button("認識", key="recog"), sg.Button("終了", key="quit")],
]

# ウィンドウ生成
WINDOW = sg.Window("Speech-To-Text sample", LAYOUT, font=FONT)


def recog():
    """リッスンする関数"""

    global RECOG_TEXT

    # 音声録音を指定秒数実行
    AUDIO = sd.rec(
        int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=N_CHANNEL
    )
    sd.wait()

    # 一旦ファイルに書き込む
    sf.write(
        file=OUTPUT_FILE,
        data=AUDIO,
        samplerate=SAMPLE_RATE,
        format="WAV",
        subtype="PCM_16",
    )

    # 収録した音声に対して音声認識実行
    with sr.AudioFile(OUTPUT_FILE) as source:
        audio = r.listen(source)  # 音声取得
        try:
            text = r.recognize_google(audio, language="ja-JP")
            WINDOW["-RECOG_TEXT-"].Update("認識結果: " + text)
            RECOG_TEXT = text

        except sr.UnknownValueError:
            WINDOW["-RECOG_TEXT-"].Update("認識に失敗しました")


# 参考　https://sannabocona.hatenablog.com/entry/wikipedia.api_python1
def wikipediaSearch(search_text):
    """Wikipediaを検索する関数

    引数:
        search_text: 検索クエリ
    """
    response_string = ""
    wikipedia.set_lang("ja")

    search_response = wikipedia.search(search_text)
    if not search_response:
        response_string = "その単語は登録されていません。"
        return response_string
    try:
        wiki_page = wikipedia.page(search_response[0])
    except Exception as e:
        response_string = "エラーが発生しました。\n{}\n{}".format(e.message, str(e))
        return response_string

    wiki_content = wiki_page.content

    # 最初の句点まで
    response_string += wiki_content[0 : wiki_content.find("。")] + "。\n"

    # 丸カッコを除く
    response_string = re.sub("（.+?）", "", response_string)

    return response_string


# イベントループ
while True:

    # イベント読み込み
    event, values = WINDOW.read()

    if event == sg.WINDOW_CLOSED or event == "quit":
        break

    elif event == "recog":
        recog()  # 音声認識
        text = wikipediaSearch(RECOG_TEXT)  # wikipediaを検索
        WINDOW["wiki_result"].Update(text)
        tts = gTTS(text, lang="ja")  # 音声合成（テキストデータ→音声データ）
        tts.save(OUT_MP3)  # mp3形式でファイルを保存
        subprocess.run("afplay " + OUT_MP3, shell=True)  # 再生


# ウィンドウを閉じて終了
WINDOW.close()
