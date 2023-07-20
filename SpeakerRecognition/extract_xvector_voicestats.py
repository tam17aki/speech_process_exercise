#!/usr/bin/env python3

""" 音声情報処理 n本ノック !! """

# MIT License

# Copyright (C) 2023 by Akira TAMAMORI

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
# xvector-jtubespeechの事前学習済モデルに基づくxvector抽出

import glob
import os

import librosa
import numpy as np
import torch
from hydra import compose, initialize
from progressbar import progressbar as prg
from torchaudio.compliance import kaldi
from xvector_jtubespeech import XVector


def extract_xvector(cfg):
    "Extract XVectors from wave file."

    feat_dir = os.path.join(cfg.xvector.root_dir, cfg.xvector.feat_dir)
    os.makedirs(feat_dir, exist_ok=True)
    data_dir = os.path.join(cfg.xvector.root_dir, cfg.xvector.data_dir)

    model = XVector(
        os.path.join(
            cfg.xvector.root_dir, cfg.xvector.model_dir, cfg.pretrained.file_name
        )
    )
    for actor in cfg.actor:
        out_dir = os.path.join(feat_dir, actor)
        os.makedirs(out_dir, exist_ok=True)
        for emotion in cfg.emotion:
            data_path = data_dir + actor + "_" + emotion
            wav_list = glob.glob(data_path + f"/{actor}_{emotion}_*.wav")
            for wav_file in prg(
                wav_list, prefix=f"Extract xvectors from {emotion} of {actor}: "
            ):
                wav, _ = librosa.load(wav_file, sr=cfg.feature.sample_rate)
                basename = os.path.basename(wav_file)
                basename, _ = os.path.splitext(basename)
                wav = torch.from_numpy(wav.astype(np.float32)).unsqueeze(0)
                mfcc = kaldi.mfcc(
                    wav,
                    num_ceps=cfg.feature.num_ceps,
                    num_mel_bins=cfg.feature.num_melbins,
                )
                mfcc = mfcc.unsqueeze(0)
                xvector = model.vectorize(mfcc)
                xvector = xvector.to("cpu").detach().numpy().copy()[0]
                out_path = os.path.join(out_dir, f"{basename}.npy")
                np.save(out_path, xvector)


if __name__ == "__main__":
    with initialize(version_base=None, config_path="."):
        config = compose(config_name="config")
    extract_xvector(config)
