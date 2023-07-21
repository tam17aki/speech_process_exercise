#!/usr/bin/env python3
"""Sample script for extraction of x-vector from a audio (monaural wav).

Copyright (C) 2022 sarulab-speech
Copyright (C) 2023 by Akira TAMAMORI

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

import numpy as np
import torch
from scipy.io import wavfile
from torchaudio.compliance import kaldi
from xvector_jtubespeech import XVector


def extract_xvector(model, wav):
    """Extract x-vector."""
    # extract mfcc
    wav = torch.from_numpy(wav.astype(np.float32)).unsqueeze(0)
    mfcc = kaldi.mfcc(wav, num_ceps=24, num_mel_bins=24)  # [1, T, 24]
    mfcc = mfcc.unsqueeze(0)

    # extract xvector
    xvector = model.vectorize(mfcc)  # (1, 512)
    xvector = xvector.to("cpu").detach().numpy().copy()[0]
    return xvector


def main():
    """Perform extraction demo."""
    _, wav = wavfile.read("in.wav")  # 16kHz mono
    model = XVector("xvector.pth")  # pretrained model
    xvector = extract_xvector(model, wav)
    print(xvector.shape)  # (512, )


if __name__ == "__main__":
    main()
