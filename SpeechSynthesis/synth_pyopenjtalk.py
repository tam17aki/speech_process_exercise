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
# pyopenjtalkによるテキスト音声合成のサンプルスクリプト

import numpy as np
import pyopenjtalk
import sounddevice as sd


class TextToSpeech:
    """Class for Text-to-Speech."""

    def __init__(self, run_marine=False):
        """Initialize the class.

        run_marine (bool): enabel MARINE model to improve Japanese accent estimation.
        """
        self.audio = None
        self.sr = None
        self.run_marine = run_marine

    def generate(self, text):
        """Perform text-to-speech."""
        self.audio, self.sr = pyopenjtalk.tts(text, run_marine=self.run_marine)

    def play(self):
        """Play synthesized speech."""
        audio = self.audio / np.abs(self.audio).max()
        audio = audio * (np.iinfo(np.int16).max / 2 - 1)
        audio = audio.astype(np.int16)
        sd.play(audio, self.sr)
        sd.sleep(int(1000 * len(audio) / self.sr))


def main(text: str = "こんにちは", run_marine=False):
    """main module."""
    tts = TextToSpeech(run_marine)
    tts.generate(text)
    tts.play()


if __name__ == "__main__":
    print("MARINEによるアクセント推定 ON")
    main("いつでも話しかけてくださいね。", True)

    print("MARINEによるアクセント推定 OFF")
    main("いつでも話しかけてくださいね。", False)
