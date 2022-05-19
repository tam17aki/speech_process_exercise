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
# ttslearnによる複数話者のテキスト音声合成

import numpy as np
import PySimpleGUI as sg  # GUI構築のライブラリ
import sounddevice as sd  # 録音・再生系のライブラリ
import speech_recognition as sr  # 音声認識のライブラリ
import torch  # 深層学習のライブラリ
from ttslearn.pretrained import create_tts_engine  # 音声合成ライブラリ

if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")

# Windowのサイズ (横, 縦) 単位ピクセル
WINDOW_SIZE = (530, 200)

# 音声合成エンジン構築
PWG_ENGINE = create_tts_engine("multspk_tacotron2_hifipwg_jvs24k", device=DEVICE)

# 話者ID
DEFAULT_SPK = "spk01"  # 初期話者

# 話者IDから話者名へ変換する辞書
ID2SPK = {
    "spk01": "話者01",
    "spk02": "話者02",
    "spk03": "話者03",
    "spk04": "話者04",
    "spk05": "話者05",
    "spk06": "話者06",
    "spk07": "話者07",
    "spk08": "話者08",
    "spk09": "話者09",
    "spk10": "話者10",
}

# 話者IDから話者モデル名へ変換する辞書
SPK2ID = {
    "spk01": "jvs010",
    "spk02": "jvs020",
    "spk03": "jvs030",
    "spk04": "jvs040",
    "spk05": "jvs050",
    "spk06": "jvs060",
    "spk07": "jvs070",
    "spk08": "jvs080",
    "spk09": "jvs090",
    "spk10": "jvs100",
}

SPK_ID = PWG_ENGINE.spk2id[SPK2ID[DEFAULT_SPK]]

# 話者選択用のフレーム
FONT = ("Arial", 20)
FRAME_SPK = sg.Frame(
    layout=[
        [
            sg.Button("話者01", key="spk01", font=FONT),
            sg.Button("話者02", key="spk02", font=FONT),
            sg.Button("話者03", key="spk03", font=FONT),
            sg.Button("話者04", key="spk04", font=FONT),
            sg.Button("話者05", key="spk05", font=FONT),
        ],
        [
            sg.Button("話者06", key="spk06", font=FONT),
            sg.Button("話者07", key="spk07", font=FONT),
            sg.Button("話者08", key="spk08", font=FONT),
            sg.Button("話者09", key="spk09", font=FONT),
            sg.Button("話者10", key="spk10", font=FONT),
        ],
        [
            sg.Text(
                "現在の話者：{}".format(ID2SPK[DEFAULT_SPK]),
                font=("Arial", 15),
                key="SPK_NAME",
            )
        ],
    ],
    title="話者選択",
    font=("Arial", 16),
    element_justification="center",
    title_location=sg.TITLE_LOCATION_TOP,
    key="-CHGSPK-",
)

# 各パーツのレイアウトを設定
# ウィンドウの下側に向かって、先頭から順に配置される
LAYOUT = [
    [sg.InputText("音声合成のサンプルです", size=(35, 1), key="-RECOG_TEXT-", font=FONT)],
    [
        FRAME_SPK,  # 話者選択用のフレーム
        sg.Column(  # ボタンを縦に並べるにはColumn関数を用いる
            [
                [sg.Button("合成", key="-SYNTH-", target="-RECOG_TEXT-", font=FONT)],
                [sg.Button("保存", key="-SAVE-", font=FONT)],
                [sg.Button("終了", key="-QUIT-", font=FONT)],
            ]
        ),
    ],
]

WINDOW = sg.Window("音声合成のGUIサンプルプログラム", LAYOUT, finalize=True, size=WINDOW_SIZE)


def change_spk(spk):
    """話者変更."""
    global SPK_ID
    SPK_ID = PWG_ENGINE.spk2id[SPK2ID[spk]]
    WINDOW["SPK_NAME"].Update("現在の話者：{}".format(ID2SPK[spk]))


while True:  # 無限ループにすることでGUIは起動しつづける
    event, values = WINDOW.read()  # イベントと「値」を取得

    # windowを閉じるか 終了ボタンを押したら終了
    if event in (sg.WIN_CLOSED, "-QUIT-"):
        break

    elif event in (
        "spk01",
        "spk02",
        "spk03",
        "spk04",
        "spk05",
        "spk06",
        "spk07",
        "spk08",
        "spk09",
        "spk10",
    ):
        # 話者変更
        change_spk(event)

    # テキスト音声合成
    elif event in ("-SYNTH-"):

        # 入力テキストを取得
        text = values["-RECOG_TEXT-"]

        # テキストから音声合成
        wav, sr = PWG_ENGINE.tts(text, spk_id=SPK_ID)

        # 音割れ防止
        wav = (wav / np.abs(wav).max()) * (np.iinfo(np.int16).max / 2 - 1)

        # 再生
        sd.play(wav.astype(np.int16), sr)
        sd.sleep(int(1000 * len(wav) / sr))

# ウィンドウを閉じて終了
WINDOW.close()
