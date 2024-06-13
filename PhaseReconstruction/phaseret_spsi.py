# -*- coding: utf-8 -*-
"""Demonstration of Single Pass Spectrogram Inversion (SPSI).

Copyright (C) 2024 by Akira TAMAMORI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
from pathlib import Path

import numpy as np
import soundfile as sf
from oct2py import octave
from scipy import signal


def main():
    """Reconstruct phase by using SPSI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ltfat_dir", type=str, default="/work/tamamori/ltfat-main")
    parser.add_argument("--win_len", type=int, default=512)
    parser.add_argument("--hop_len", type=int, default=128)
    parser.add_argument("--fft_len", type=int, default=512)
    parser.add_argument("--window", type=str, default="hann")
    parser.add_argument("--in_wavdir", type=str, default="/home/tamamori")
    parser.add_argument("--in_wav", type=str, default="in.wav")
    parser.add_argument("--out_wavdir", type=str, default="/home/tamamori")
    parser.add_argument("--out_wav", type=str, default="out.wav")
    args = parser.parse_args()

    # initialization
    octave.addpath(octave.genpath(args.ltfat_dir))
    octave.ltfatstart(0)  # 引数の0を省略するとoct2pyのエラーでこける
    octave.phaseretstart(0)  # 引数の0を省略するとoct2pyのエラーでこける

    # compute magnitude spectrum
    audio, rate = sf.read(Path(args.in_wavdir, args.in_wav))
    stfft = signal.ShortTimeFFT(
        win=signal.get_window(args.window, args.win_len),
        hop=args.hop_len,
        fs=rate,
        mfft=args.fft_len,
    )
    mag_spec = np.abs(stfft.stft(audio))

    # reconstruct phase spectrum with SPSI
    reconst_spec = octave.spsi(mag_spec, args.hop_len, args.win_len)
    audio = stfft.istft(reconst_spec)
    sf.write(Path(args.out_wavdir, args.out_wav), audio, rate)


if __name__ == "__main__":
    main()
