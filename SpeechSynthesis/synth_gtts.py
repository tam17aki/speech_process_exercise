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
# gTTSによるテキスト音声合成のサンプルスクリプト

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


class TextToSpeech:
    """Class for Text-to-Speech."""

    def __init__(self, lang: str = "ja", out_file: str = "/tmp/tts.mp3"):
        """Initialize the class."""
        self.lang = lang
        self.out_file = out_file

    def generate(self, text):
        """Perform text-to-speech."""
        tts = gTTS(text, lang=self.lang)
        tts.save(self.out_file)  # save audio in mp3 format

    def play(self):
        """Play synthesized speech."""
        audio_data = AudioSegment.from_mp3(self.out_file)
        play(audio_data)


def main(text: str = "こんにちは"):
    """main module."""
    tts = TextToSpeech()
    tts.generate(text)
    tts.play()


if __name__ == "__main__":
    main("こんにちは")
