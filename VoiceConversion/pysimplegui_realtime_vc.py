#!/usr/bin/env python3

""" 音声情報処理 n本ノック !! """

# Copyright (c) 2020 peisuke
# Copyright (C) 2022 by Akira TAMAMORI

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Commentary:
# Real-time voice conversion by using PyAudio and PySimpleGUI.

import threading
import time

import numpy as np
import pyaudio
import PySimpleGUI as sg
import pyworld
from scipy import signal

CHUNK = 2048
RATE = 16000
CHANNEL = 1

pAud = pyaudio.PyAudio()
SHORT_MAX = 32767
SHORT_MIN = -32768
EPSIRON = 1.0e-6
SILENCE = 0

VOLUME = 10  # 再合成された音声の音量調整 （整数である必要！）

FONT = "Any 16"
WINSIZE = (512, 256)

TEXT_CONFIG = sg.Text("Scale", font=("Ricty", 15))
SLIDER_CONFIG = sg.Slider(
    range=(0.5, 2.0),
    default_value=1.0,
    resolution=0.1,
    orientation="h",
    size=(35, None),
    pad=((6, 0), (0, 10)),
    key="-PITCH-",
    enable_events=True,
)
FRAME_VC = sg.Frame(
    layout=[
        [
            TEXT_CONFIG,
            SLIDER_CONFIG,
        ],
    ],
    title="Change pitch and timber",
    font=("Ricty", 20),
    element_justification="center",
)

LAYOUT = [
    [
        sg.Graph(
            canvas_size=WINSIZE,
            graph_bottom_left=(0, -10),
            graph_top_right=(int(CHUNK / 2), 300),
            background_color="white",
            key="-GRAPH-",
        ),
        [FRAME_VC],
    ],
    [
        sg.Button("Listen", key="-LISTEN-", font=FONT),
        sg.Button("Stop", key="-STOP-", font=FONT, disabled=True),
        sg.Button("Exit", key="-EXIT-", font=FONT),
    ],
]
WINDOW = sg.Window("Waveform plot", LAYOUT, finalize=True)
GRAPH = WINDOW["-GRAPH-"]
STREAM = None
WORKER_THREAD = None
AUDIO_FILTER = None
AUDIODATA = np.array([])
TIMEOUT = 30

F0_SCALE = 1.8  # 声の高さの調整 : 2倍にすれば1オクターブ上に、0.5倍にすれば1オクターブ下に
SP_SCALE = 0.72  # 声色の調整 (> 0.0)


def convert(signal, scale):
    """Perform voice conversion."""
    f0_scale = scale
    sp_scale = np.power(f0_scale, 1.0 / 3)
    sample_rate = RATE

    f0, t = pyworld.dio(signal, sample_rate)
    f0 = pyworld.stonemask(signal, f0, t, sample_rate)
    sp = pyworld.cheaptrick(signal, f0, t, sample_rate)
    ap = pyworld.d4c(signal, f0, t, sample_rate)

    modified_f0 = f0_scale * f0

    # Formant shift
    modified_sp = np.zeros_like(sp)
    sp_range = int(modified_sp.shape[1] * sp_scale)
    for f in range(modified_sp.shape[1]):
        if f < sp_range:
            modified_sp[:, f] = sp[:, int(f / sp_scale)]
        else:
            modified_sp[:, f] = sp[:, f]

    y = pyworld.synthesize(modified_f0, modified_sp, ap, sample_rate)

    return y


# https://github.com/peisuke/babiniku/blob/master/scripts/voice_converter.py
class WorkerThread(threading.Thread):
    """ """

    def __init__(self, block_length, margin_length):
        super(WorkerThread, self).__init__()
        self.is_stop = False
        self.lock = threading.Lock()
        self.buffer = []
        self.result = []

        self.prev_samples = []

        self.f0_scale = 1.0

    def stop(self):
        self.is_stop = True
        self.join()

    def run(self):
        while not self.is_stop:
            # buffer : list of CHUNKS
            # buffer[0] = {"data": array of CHUNK samples}
            # buffer[1] = {"data": array of CHUNK samples}
            # ...
            # buffer[block_size - 1] = {"data": array of 1024 samples}
            if len(self.buffer) > 0:
                with self.lock:
                    # take the leading CHUNK and apply voice conversion.
                    buf = self.buffer[0]
                    self.buffer = self.buffer[1:]

                chunk_size = len(buf[0]["data"])
                sample = np.concatenate([b["data"] for b in buf])

                sample = sample.astype(np.float64)
                sample = convert(sample, self.f0_scale)

                # overlap and add
                self.prev_samples.append(sample)
                length = len(sample)

                weight = signal.hann(length)
                caches = []
                wcaches = []
                for i, sample in enumerate(self.prev_samples):
                    pos = (len(self.prev_samples) - i) * chunk_size
                    if len(sample) >= pos + chunk_size:
                        cache = sample[pos : pos + chunk_size]
                        wcache = weight[pos : pos + chunk_size]
                        caches.append(cache)
                        wcaches.append(wcache)

                caches = np.asarray(caches)
                wcaches = np.asarray(wcaches)
                wcaches /= wcaches.sum(axis=0)

                # compute weighted sum.
                sample = np.sum(wcaches * caches, axis=0)

                # prev_samplesは最大で16個のチャンクブロックを保持する
                if len(self.prev_samples) >= 16:
                    self.prev_samples = self.prev_samples[1:]

                with self.lock:
                    self.result.extend(sample.tolist())
            else:
                time.sleep(0.01)

    def push_chunk(self, chunk):
        """Push blocks (= CHUNK * block_size) into buffer."""
        with self.lock:
            self.buffer.append(chunk)

    def pop_chunk(self, chunk_size):
        result = None
        with self.lock:
            if len(self.result) >= chunk_size:
                result = np.array(self.result[:chunk_size])
                self.result = self.result[chunk_size:]

        return result

    def set_f0_scale(self, scale):
        self.f0_scale = scale


class AudioFilter:
    def __init__(self, worker, block_length, margin_length):
        self.p = pyaudio.PyAudio()
        input_index, output_index = self.get_channels(self.p)

        self.channels = CHANNEL
        self.rate = RATE
        self.format = pyaudio.paInt16
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            frames_per_buffer=CHUNK,
            input_device_index=input_index,
            output_device_index=output_index,
            output=True,
            input=True,
            stream_callback=self.callback,
        )

        self.age = 0
        self.index = 0
        self.chunk = []
        self.buffer = []
        self.worker = worker
        self.f0scale = 1.0

        self.block_length = block_length
        self.margin_length = margin_length

    def get_channels(self, p):
        input_index = self.p.get_default_input_device_info()["index"]
        output_index = self.p.get_default_output_device_info()["index"]
        return input_index, output_index

    def set_f0_scale(self, scale):
        self.worker.set_f0_scale(scale)

    def callback(self, in_data, frame_count, time_info, status):
        global AUDIODATA
        decoded_data = np.frombuffer(in_data, np.int16).copy()
        AUDIODATA = decoded_data.copy()
        chunk_size = len(decoded_data)

        decoded_data = decoded_data.reshape(-1, CHUNK)
        for c in decoded_data:
            self.chunk.append({"data": c})
            # self.index += 1

        if decoded_data.max() > SILENCE:
            self.age = self.block_length
        else:
            self.age = max(0, self.age - 1)

        if self.age == 0:
            self.chunk = self.chunk[-self.margin_length :]
        else:
            while len(self.chunk) >= self.block_length:
                # (CHUNKサイズ1024 × ブロックサイズ)のデータをワーカーに送る
                # つまり1ブロックあたりCHUNKのデータサンプル
                self.worker.push_chunk(self.chunk[0 : self.block_length])

                # 変数chunkは先頭の1ブロック(CHUNK個のデータ)を削除し、
                # 依然として7ブロックを保持しておく
                # →次のcallbackで呼ばれるため
                self.chunk = self.chunk[1:]

        ret = self.worker.pop_chunk(chunk_size)

        # Get head from current list
        if ret is not None:
            data = VOLUME * ret.astype(np.int16)
        else:
            data = np.zeros(chunk_size, dtype=np.int16)

        out_data = data.tobytes()

        return (out_data, pyaudio.paContinue)

    def close(self):
        self.p.terminate()


def listen():
    """Start recording."""

    WINDOW["-STOP-"].update(disabled=False)
    WINDOW["-LISTEN-"].update(disabled=True)

    block_length = 8
    margin_length = 1

    worker_th = WorkerThread(block_length, margin_length)
    worker_th.daemon = True
    worker_th.start()

    af = AudioFilter(worker_th, block_length, margin_length)
    af.stream.start_stream()

    return af, worker_th


def stop():
    """Stop recording."""
    if AUDIO_FILTER is not None:
        WORKER_THREAD.stop()
        AUDIO_FILTER.stream.stop_stream()
        AUDIO_FILTER.stream.close()
        WINDOW["-STOP-"].update(disabled=True)
        WINDOW["-LISTEN-"].update(disabled=False)


def plot_fftspec():
    """Plot FFT spectrum."""
    GRAPH.erase()  # re-draw

    # draw axix
    GRAPH.draw_line((0, 0), (CHUNK, 0))
    GRAPH.draw_line((0, SHORT_MIN), (0, SHORT_MIN))

    # compute fft spectrum
    fftspec = np.fft.fft(AUDIODATA)
    fftspec = np.abs(fftspec) ** 2
    fftspec = fftspec[0 : int(CHUNK / 2)]
    fftspec = 20 * np.log10(fftspec + EPSIRON)

    # plot spectrum
    prev_x = prev_y = None
    for x, y in enumerate(fftspec):
        if prev_x is not None:
            GRAPH.draw_line((prev_x, prev_y), (x, y), color="red")
        prev_x, prev_y = x, y


while True:
    event, values = WINDOW.read(timeout=TIMEOUT)

    if event in (sg.WIN_CLOSED, "-EXIT-"):
        stop()
        if AUDIO_FILTER is not None:
            AUDIO_FILTER.close()
        break
    if event == "-LISTEN-":
        AUDIO_FILTER, WORKER_THREAD = listen()
    elif event == "-STOP-":
        stop()
    elif AUDIODATA.size != 0:
        plot_fftspec()

    # timeout event
    if AUDIO_FILTER is not None:
        AUDIO_FILTER.set_f0_scale(values["-PITCH-"])

WINDOW.close()
