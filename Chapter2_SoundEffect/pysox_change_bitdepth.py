#!/usr/bin/env python3

""" 音声情報処理 n本ノック !! """

# MIT License

# Copyright (C) 2020 by Akira TAMAMORI

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
# - PySoxを用いた音声情報処理シリーズ
# - 量子化ビット数を変更

import sox

IN_WAVE_FILE = "mono.wav"          # モノラル音声 (量子化ビット数 16bit)
OUT_WAVE_FILE = "out.wav"          # モノラル音声

BITDEPTH = 8

# create trasnformer (単一ファイルに対する重ねがけ)
transformer = sox.Transformer()

# 量子化ビット数を8bitに変更
transformer.convert(bitdepth=BITDEPTH)
transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE)
