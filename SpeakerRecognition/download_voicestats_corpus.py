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
# subprocesモジュールを介したwgetによる声優統計コーパスダウンロード

import os
import subprocess

from hydra import compose, initialize


def get_corpus(cfg):
    """Download voice-statistics corpurs."""
    corpus_url = cfg.xvector.corpus_url
    data_dir = os.path.join(cfg.xvector.root_dir, cfg.xvector.data_dir)
    os.makedirs(data_dir, exist_ok=True)

    subprocess.run(
        "echo -n Downloading voice statistics corpus ...",
        text=True,
        shell=True,
        check=True,
    )
    for actor in cfg.actor:  # "tsuchiya", "fujitou", "uemura"
        for emotion in cfg.emotion:  # "angry", "happy", "normal"
            command = "wget " + "-P " + "/tmp/" + " " + corpus_url
            tar_file = actor + "_" + emotion + ".tar.gz"
            command = command + tar_file
            subprocess.run(
                command, text=True, shell=True, capture_output=True, check=True
            )
            command = "cd " + data_dir + "; " + "tar -xzvf " + "/tmp/" + tar_file
            subprocess.run(
                command, text=True, shell=True, capture_output=True, check=True
            )
    print(" done.")


if __name__ == "__main__":
    with initialize(version_base=None, config_path="."):
        config = compose(config_name="config")
    get_corpus(config)
