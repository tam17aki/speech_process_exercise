"""PySimpleGUIにより音声を録音し、音声の分析合成を実施する.
    波形とスペクトログラムもプロット可能.
"""
import queue
import sys
import threading
import time

import librosa  # 音声分析のライブラリ
import matplotlib.pyplot as plt  # グラフ描画のライブラリ
import numpy as np
import PySimpleGUI as sg  # GUI構築のライブラリ
import pysptk  # 音声分析合成のライブラリ
import sounddevice as sd  # 録音・再生系のライブラリ
import soundfile as sf  # 読み込み・書き出しのライブラリ
import speech_recognition as sr  # 音声認識のライブラリ
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pysptk.synthesis import MLSADF, Synthesizer  # 音声分析合成のライブラリ

# Windowのサイズ (横, 縦) 単位ピクセル
WINDOW_SIZE = (1000, 650)

# 出力先の音声ファイル名
OUTPUT_FILE = "/tmp/record.wav"

CHUNK = 512  # チャンクサイズ
SAMPLE_RATE = 16000  # サンプリング周波数
N_CHANNEL = 1  # チャンネル数 モノラルは1, ステレオは2
DURATION = 3  # 収録秒数
BUFFER = 0.010
BUFF = queue.Queue()

# 音声の分析条件（デフォルト）
FRAME_LENGTH = 512  # フレーム長 (point)
FFT_LENGTH = 512  # FFT長 (point)
HOP_LENGTH = 80  # フレームシフト (point)
MIN_F0 = 60  # 基本周波数の最小値 (Hz)
MAX_F0 = 240  # 基本周波数の最大値 (Hz)
ORDER = 25  # メルケプストラムの分析次数
ALPHA = 0.35  # 周波数ワーピングのパラメタ

# Canvasオブジェクト生成
CANVAS = sg.Canvas()  # PySimpleGUIのCanvasオブジェクト

# PySimpleGUI 初期化
FONT = "Any 16"
sg.theme("SystemDefault1")

# ボタンとスライダの設定
TEXT_CONFIG = {"pitch": None, "alpha": None, "tempo": None}
SLIDER_CONFIG = {"pitch": None, "alpha": None, "tempo": None}
BUTTON_CONFIG = {"pitch": None, "alpha": None, "tempo": None}
INTEXT_CONFIG = {"pitch": None, "alpha": None, "tempo": None}

TEXT_CONFIG["pitch"] = sg.Text("声の高さ", font=("Ricty", 15))
SLIDER_CONFIG["pitch"] = sg.Slider(
    range=(0.5, 2.0),
    default_value=1.0,
    resolution=0.1,
    orientation="h",
    size=(35, None),
    pad=((6, 0), (0, 10)),
    key="-PITCH-",
    enable_events=True,
)
BUTTON_CONFIG["pitch"] = sg.Button("設定", font=FONT, key="-PITCH_SET-")
INTEXT_CONFIG["pitch"] = sg.InputText(
    default_text="1.0",
    size=(4, 1),
    font="Any 14",
    key="pitch_val",
    justification="center",
)

TEXT_CONFIG["alpha"] = sg.Text("声色", font=("Ricty", 15))
SLIDER_CONFIG["alpha"] = sg.Slider(
    range=(0.0, 1.0),
    default_value=ALPHA,
    resolution=0.01,
    orientation="h",
    size=(35, None),
    pad=((36, 0), (0, 10)),
    key="-ALPHA-",
    enable_events=True,
)
BUTTON_CONFIG["alpha"] = sg.Button("設定", font=FONT, key="-ALPHA_SET-")
INTEXT_CONFIG["alpha"] = sg.InputText(
    default_text="{}".format(ALPHA),
    size=(4, 1),
    font="Any 14",
    key="alpha_val",
    justification="center",
)

TEXT_CONFIG["tempo"] = sg.Text("話速", font=("Ricty", 15))
SLIDER_CONFIG["tempo"] = sg.Slider(
    range=(0.5, 2.0),
    default_value=1.0,
    resolution=0.1,
    orientation="h",
    size=(35, None),
    pad=((36, 0), (0, 10)),
    key="-TEMPO-",
    enable_events=True,
)
BUTTON_CONFIG["tempo"] = sg.Button("設定", font=FONT, key="-RATE_SET-")
INTEXT_CONFIG["tempo"] = sg.InputText(
    default_text="1.0",
    size=(4, 1),
    font="Any 14",
    key="tempo_val",
    justification="center",
)

# ボタンとスライダをフレームにまとめる→Frameの戻り値は一つのレイアウト
FRAME_ANASYN = sg.Frame(
    layout=[
        [
            TEXT_CONFIG["pitch"],
            SLIDER_CONFIG["pitch"],
            INTEXT_CONFIG["pitch"],
            BUTTON_CONFIG["pitch"],
        ],
        [
            TEXT_CONFIG["alpha"],
            SLIDER_CONFIG["alpha"],
            INTEXT_CONFIG["alpha"],
            BUTTON_CONFIG["alpha"],
        ],
        [
            TEXT_CONFIG["tempo"],
            SLIDER_CONFIG["tempo"],
            INTEXT_CONFIG["tempo"],
            BUTTON_CONFIG["tempo"],
        ],
        [
            sg.Button("分析再合成", font=FONT, key="-ANASYN-"),
            sg.Button("分析再合成音を聞く", font=FONT, key="-PLAY_ANASYN-"),
        ],
    ],
    title="声の高さ・声色・話速を調整",
    font=("Ricty", 20),
    element_justification="left",
)

# 各パーツのレイアウトを設定
# ウィンドウの下側に向かって、先頭から順に配置される
LAYOUT = [
    [
        sg.Text(
            "早口言葉を{}秒間：赤巻紙 青巻紙 黄巻紙".format(DURATION),
            font=("Ricty", 22),
            text_color="#000000",
            background_color="#839496",
        ),
        sg.ProgressBar(
            int(DURATION * SAMPLE_RATE / CHUNK),
            orientation="h",
            bar_color=("#dc322f", "#eee8d5"),
            size=(20, 22),
            key="-PROG-",
        ),
    ],
    [
        sg.Button("再生", font=FONT, key="-PLAY-"),
        sg.Button("録音", font=FONT, key="-REC-"),
        sg.Button("停止", font=FONT, key="-STOP-"),
        sg.Button("波形表示", font=FONT, key="-PLTWAV-"),
        sg.Button("スペクトログラム表示", font=FONT, key="-PLTSPEC-"),
        sg.Button("保存", font=FONT, key="-SAVE-"),
        sg.Button("認識", font=FONT, key="-RECOG-"),
        sg.Button("終了", font=FONT, key="-EXIT-"),
    ],
    [
        sg.FileBrowse(
            "ファイルを開いて波形表示",
            font=FONT,
            key="-FILES-",
            target="-FILES-",
            file_types=((("WAVEファイル", "*.wav"),)),
            enable_events=True,
        ),
        sg.Text(
            "ここに音声認識結果が表示されます",
            font=("Ricty", 22),
            text_color="#000000",
            background_color="#eee8d5",
            size=(40, 1),
            key="-RECOG_TEXT-",
        ),
    ],
    # 描画領域
    [CANVAS],
    # 分析再合成まわり
    [FRAME_ANASYN],
]

# 各関数からアクセスするグローバル変数
VARS = {
    "window": sg.Window("音声分析のGUIサンプルプログラム", LAYOUT, finalize=True, size=WINDOW_SIZE),
    "audio": None,  # 収録済み音声（もしくはロードした音声）
    "anasyn": None,  # 分析再合成音
}


# Figure領域の確保 (Windowオブジェクト作成後)
FIGURE = plt.figure(figsize=(9, 3))
AXES = FIGURE.add_subplot(1, 1, 1)
TK_CANVAS = CANVAS.TKCanvas
FAG = FigureCanvasTkAgg(FIGURE, TK_CANVAS)


def normalize(audio):
    """音声データを正規化する"""
    audio = audio / np.abs(audio).max()
    audio = audio * (np.iinfo(np.int16).max / 2 - 1)
    audio = audio.astype(np.int16)
    return audio


def load_wav(file_name):
    """WAVファイルをロードする"""
    audio, _ = sf.read(file_name)

    # 振幅の正規化
    audio = normalize(VARS["audio"])

    VARS["audio"] = audio

    # 保存しておく
    sf.write(
        file=OUTPUT_FILE,
        data=audio,
        samplerate=SAMPLE_RATE,
        format="WAV",
        subtype="PCM_16",
    )


def play_wav():
    """WAVを再生する"""
    # 振幅の正規化
    audio = normalize(VARS["audio"])

    # 再生
    sd.play(audio, SAMPLE_RATE)

    # 再生は非同期に行われるので、明示的にsleepさせる
    sd.sleep(int(1000 * len(VARS["audio"]) / SAMPLE_RATE))


def play_stop():
    """WAV再生を停止する"""
    sd.stop()


def callback(indata, frames, time, status):
    """音声入力の度に呼び出されるコールバック関数."""
    if status:
        print(status, file=sys.stderr)

    # 入力された音声データをキューへ保存
    BUFF.put(bytes(indata))


def generator():
    """音声認識に必要な音声データを取得するための関数."""
    while True:  # キューに保存されているデータを全て取り出す
        # 先頭のデータを取得
        chunk = BUFF.get()
        if chunk is None:
            return
        data = [chunk]

        # まだキューにデータが残っていれば全て取得する
        while True:
            try:
                chunk = BUFF.get(block=False)
                if chunk is None:
                    return
                data.append(chunk)
            except queue.Empty:
                break

        # yieldにすることでキューのデータを随時取得できるようにする
        yield b"".join(data)


def record():
    """録音する関数"""
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=CHUNK,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        count = 0
        frames = []  # 連結用リスト
        audio_generator = generator()
        for content in audio_generator:
            if count >= int(DURATION * SAMPLE_RATE / CHUNK):
                break
            count = count + 1
            frames.append(np.frombuffer(content, dtype=np.int16))

    # リストの各要素を取り出し、一つの長いnumpy配列として連結 (concatenate)
    recording = np.concatenate(frames)

    # 振幅値を正規化
    recording = recording / recording.max() * np.iinfo(np.int16).max

    # 演算結果がfloatなので2byte整数に変換
    recording = recording.astype(np.int16)
    VARS["audio"] = recording


def listen():
    """リッスンする関数"""
    # 音声録音の非同期実行
    record_thread = threading.Thread(target=record, daemon=True)
    record_thread.start()  # 終了すると自動でterminateする

    # 録音している間、プログレスバーを並行して表示
    VARS["window"]["-PROG-"].update(0)
    wait_second = CHUNK / SAMPLE_RATE - BUFFER
    for i in range(int(DURATION * SAMPLE_RATE / CHUNK)):
        # プログレスバーを更新
        VARS["window"]["-PROG-"].update(i + 1)
        time.sleep(wait_second)


def recog():
    """音声認識する関数（音声データをテキストに変換）"""
    # 振幅の正規化
    audio = normalize(VARS["audio"])

    # 一旦ファイルに保存
    sf.write(
        file=OUTPUT_FILE,
        data=audio,
        samplerate=SAMPLE_RATE,
        format="WAV",
        subtype="PCM_16",
    )

    r = sr.Recognizer()
    with sr.AudioFile(OUTPUT_FILE) as source:  # ファイルから音声取得
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ja-JP")
            VARS["window"]["-RECOG_TEXT-"].Update(text)
        except sr.UnknownValueError:
            VARS["window"]["-RECOG_TEXT-"].Update("認識に失敗しました")


def plot_waveform():
    """波形をプロットする関数"""
    # 振幅の正規化
    audio = normalize(VARS["audio"])

    # 継続時間に等しい標本点の作成
    times = DURATION * (np.arange(0, len(VARS["audio"])) / len(VARS["audio"]))

    # 波形プロット
    AXES.cla()  # plotのクリア
    AXES.set_xlabel("Time (sec)")
    AXES.set_ylabel("Amplitude")
    AXES.plot(times, audio)
    FIGURE.tight_layout()

    # Canvasへ描画する
    FAG.draw()  # TkinterのCanvasに描画
    FAG.get_tk_widget().pack()  # TkinterのCanvasをレイアウトに反映


def plot_specgram():
    """スペクトログラムを表示する関数"""
    # 振幅の正規化
    audio = normalize(VARS["audio"])

    n_overlap = FFT_LENGTH - HOP_LENGTH  # オーバーラップ幅

    # スペクトログラムをプロット
    AXES.cla()  # plotのクリア
    AXES.specgram(
        audio,
        NFFT=FFT_LENGTH,
        noverlap=n_overlap,
        Fs=SAMPLE_RATE,
        cmap="jet",
    )
    AXES.set_xlabel("Time (sec)")
    AXES.set_ylabel("Frequency (Hz)")
    FIGURE.tight_layout()

    # Canvasへ描画する
    FAG.draw()  # TkinterのCanvasに描画
    FAG.get_tk_widget().pack()  # TkinterのCanvasをレイアウトに反映


def analysis_synthesis(pitch_shift=1.0, alpha=0.35, tempo=1.0):
    """音声の分析再合成

    Parameters
    ----------
    pitch_shift: float in (0.0, 1] (default=1.0)
       ピッチシフト。声の高さを何倍にするかを指定。

    alpha: float in (0.0, 1]) (default=0.35)
       声道長（喉の長さ）パラメータ。
       大人は喉が長い。子供は喉が短い。

    tempo: float in (0.0, 2) (default=1.0)
       話速パラメータ。1.0は話速変更なし。
       0.5は話速が2倍、2.0は話速が半分に対応
    """
    hop_length = int(HOP_LENGTH * tempo)

    audio = normalize(VARS["audio"])

    # 音声の切り出しと窓掛け
    frames = (
        librosa.util.frame(
            audio, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH
        )
        .astype(np.float64)
        .T
    )
    frames *= pysptk.blackman(FRAME_LENGTH)  # 窓掛け（ブラックマン窓）

    # ピッチ抽出
    pitch = pysptk.swipe(
        audio.astype(np.float64),
        fs=SAMPLE_RATE,
        hopsize=HOP_LENGTH,
        min=MIN_F0,
        max=MAX_F0,
        otype="pitch",
    )

    # 励振源信号(声帯音源)の生成
    source_excitation = pysptk.excite(pitch * (1.0 / pitch_shift), hop_length)

    # メルケプストラム分析（＝スペクトル包絡の抽出）
    mc = pysptk.mcep(frames, ORDER, ALPHA)

    # メルケプストラム係数からMLSAディジタルフィルタ係数に変換
    mlsa_coef = pysptk.mc2b(mc, ALPHA)

    # MLSAフィルタの作成
    synthesizer = Synthesizer(MLSADF(ORDER, alpha), hop_length)

    # 音声の再合成
    VARS["anasyn"] = synthesizer.synthesis(source_excitation, mlsa_coef)


def play_anasyn():
    """分析再合成音を再生する"""
    audio = normalize(VARS["anasyn"])
    sd.play(audio, SAMPLE_RATE)
    sd.sleep(int(1000 * len(audio) / SAMPLE_RATE))


def event_play_record(event):
    """再生・録音系のイベント処理"""

    # 音声を再生
    if event == "-PLAY-":
        if VARS["audio"] is None or len(VARS["audio"]) == 0:
            sg.popup("Audio data must not be empty!", font=FONT)
        else:
            play_wav()

    # 再生を停止
    elif event == "-STOP-":
        if VARS["audio"] is None or len(VARS["audio"]) == 0:
            sg.popup("Audio data must not be empty!", font=FONT)
        else:
            play_stop()

    # 録音
    elif event == "-REC-":
        listen()


def event_plot_graph(event, values):
    """プロット系のイベント処理"""

    # 波形プロット
    if event == "-PLTWAV-":
        if values["-FILES-"] != "":
            load_wav(values["-FILES-"])
        if VARS["audio"] is None or len(VARS["audio"]) == 0:
            sg.popup("Audio data must not be empty!", font=FONT)
        else:
            plot_waveform()

    # スペクトログラムプロット
    elif event == "-PLTSPEC-":
        if values["-FILES-"] != "":
            load_wav(values["-FILES-"])
        if VARS["audio"] is None or len(VARS["audio"]) == 0:
            sg.popup("Audio data must not be empty!", font=FONT)
        else:
            plot_specgram()

    # ファイルを開いて波形プロット
    elif event == "-FILES-":
        load_wav(values["-FILES-"])
        plot_waveform()


def event_anasyn(event, values):
    """分析合成系のイベント処理"""
    # 音声の分析再合成
    if event == "-ANASYN-":
        if VARS["audio"] is None or len(VARS["audio"]) == 0:
            sg.popup("Audio data must not be empty!", font=FONT)
        else:
            analysis_synthesis(values["-PITCH-"], values["-ALPHA-"], values["-TEMPO-"])

    # テキストボックスの値をスライダーに反映（ピッチ）
    elif event == "-PITCH_SET-":  # 「設定」ボタンを押す
        VARS["window"]["-PITCH-"].Update(values["pitch_val"])

    # スライダーの値をテキストボックスに反映（ピッチ）
    elif event == "-PITCH-":  # スライダーを動かす
        VARS["window"]["pitch_val"].Update(values["-PITCH-"])

    # テキストボックスの値をスライダーに反映（alpha）
    elif event == "-ALPHA_SET-":
        VARS["window"]["-ALPHA-"].Update(values["alpha_val"])

    # スライダーの値をテキストボックスに反映（alpha）
    elif event == "-ALPHA-":  # スライダーを動かす
        VARS["window"]["alpha_val"].Update(values["-ALPHA-"])

    # テキストボックスの値をスライダーに反映（テンポ）
    elif event == "-TEMPO_SET-":
        VARS["window"]["-TEMPO-"].Update(values["tempo_val"])

    # スライダーの値をテキストボックスに反映（テンポ）
    elif event == "-TEMPO-":  # スライダーを動かす
        VARS["window"]["tempo_val"].Update(values["-TEMPO-"])

    # 分析再合成を聞く
    elif event == "-PLAY_ANASYN-":
        if VARS["anasyn"] is None or len(VARS["anasyn"]) == 0:
            sg.popup("Audio data must not be empty!", font=FONT)
        else:
            play_anasyn()


def event_recog(event, values):
    """音声認識系のイベント処理"""
    if event == "-RECOG-":
        if VARS["audio"] is None or len(VARS["audio"]) == 0:
            sg.popup("Audio data must not be empty!", font=FONT)
        else:
            recog()


def finalize():
    """終了処理"""
    # Windowを閉じる
    VARS["window"].close()


def mainloop():
    """メインのループ"""

    while True:  # 無限ループにすることでGUIは起動しつづける
        event, values = VARS["window"].read()  # イベントと「値」を取得

        # windowを閉じるか 終了ボタンを押したら終了
        if event in (sg.WIN_CLOSED, "-EXIT-"):
            finalize()
            break

        # 再生・録音系イベント
        if event in ("-PLAY-", "-STOP-", "-REC-"):
            event_play_record(event)

        # プロット系イベント
        elif event in ("-PLTWAV-", "-PLTSPEC-", "-FILES-"):
            event_plot_graph(event, values)

        # 分析再合成系イベント
        elif event in (
            "-ANASYN-",
            "-PITCH-",
            "-ALPHA-",
            "-TEMPO-",
            "-PITCH_SET-",
            "-ALPHA_SET-",
            "-TEMPO_SET-",
            "-PLAY_ANASYN-",
        ):
            event_anasyn(event, values)

        # 音声認識系イベント
        elif event in ("-RECOG-"):
            event_recog(event, values)


if __name__ == "__main__":
    # GUI起動
    mainloop()
