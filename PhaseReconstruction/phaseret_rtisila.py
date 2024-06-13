# -*- coding: utf-8 -*-
"""Demonstration of Real-Time Iterative Spectrogram Inversion with Look Ahead (RTISILA).

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
import warnings
from pathlib import Path

import numpy as np
import soundfile as sf
from oct2py import octave
from scipy import signal

warnings.filterwarnings("ignore")


def main():
    """Reconstruct phase by using RTISILA."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ltfat_dir", type=str, default="/work/tamamori/ltfat-main")
    parser.add_argument("--win_len", type=int, default=512)
    parser.add_argument("--hop_len", type=int, default=128)
    parser.add_argument("--fft_len", type=int, default=512)
    parser.add_argument("--window", type=str, default="hann")
    parser.add_argument("--n_lookahead", type=int, choices=range(0, 4), default=3)
    parser.add_argument("--in_wavdir", type=str, default="/home/tamamori")
    parser.add_argument("--in_wav", type=str, default="in.wav")
    parser.add_argument("--out_wavdir", type=str, default="/home/tamamori")
    parser.add_argument("--out_wav", type=str, default="out.wav")
    args = parser.parse_args()

    # initialization
    octave.addpath(octave.genpath(args.ltfat_dir))

    # compute magnitude spectrum
    audio, rate = sf.read(Path(args.in_wavdir, args.in_wav))
    stfft = signal.ShortTimeFFT(
        win=signal.get_window(args.window, args.win_len),
        hop=args.hop_len,
        fs=rate,
        mfft=args.fft_len,
    )
    mag_spec = np.abs(stfft.stft(audio))
    _, n_frame = mag_spec.shape
    dgtlen = octave.dgtlength(n_frame * args.hop_len, args.hop_len, args.win_len)
    if dgtlen > n_frame * args.hop_len:
        ratio = (dgtlen - n_frame * args.hop_len) // args.hop_len
        mag_spec = np.pad(mag_spec, ((0, 0), (int(ratio), 0)))

    # reconstruct phase spectrum with RTISILA
    gabwin = octave.gabwin(args.window, args.hop_len, args.win_len, args.win_len)
    reconst_spec = octave.rtisila(
        mag_spec, gabwin, args.hop_len, args.win_len, "lookahead", args.n_lookahead
    )
    audio = stfft.istft(reconst_spec)
    sf.write(Path(args.out_wavdir, args.out_wav), audio, rate)


if __name__ == "__main__":
    main()
