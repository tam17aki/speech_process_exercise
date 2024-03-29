# 準備運動（音声読み込み・書き込み・波形プロットなど）
## はじめに
```
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
pip3 install sounddevice
pip3 install pydub
pip3 install ffmpeg-python
```

## 使用データ
以下からダウンロード
- [in.wav](https://drive.google.com/file/d/1lsN-is31x_snFBTNGR05pQwX9RhzC8sb/view?usp=sharing)
- [mono.wav](https://drive.google.com/file/d/1_nKAtHg4qsY0HMdLxrYsVywqDqdjY9GA/view?usp=sharing)
- [stereo.wav](https://drive.google.com/file/d/1V1Uwb1UAD51ouy9t0B89lWsDjErFPSpZ/view?usp=sharing)

## ファイル一覧
### Python スクリプト
- wavファイルの読み込みと書き込み
  - waveモジュールによる読み込みと書き込み [wave_read_write.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_read_write.py)
  - scipyのwavfileモジュールによる読み込みと書き込み [wave_read_write_scipy.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_read_write_scipy.py)
- wavファイルとmp3ファイルの相互変換
  - pydubモジュールによるwavからmp3へのエクスポート [pydub_wav_to_mp3.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/pydub_wav_to_mp3.py)
  - pydubモジュールによるmp3からwavへのエクスポート [pydub_mp3_to_wav.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/pydub_mp3_to_wav.py)
  - ffmpeg-pythonモジュールによるwavからmp3へのエクスポート [ffmpeg_wav_to_mp3.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/ffmpeg_wav_to_mp3.py)
  - ffmpeg-pythonモジュールによるmp3からwavへのエクスポート [ffmpeg_mp3_to_wav.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/ffmpeg_mp3_to_wav.py)
- サンプリング周波数を変更したwavファイルの作成 [wave_change_framerate.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_change_framerate.py)
- 量子化ビット数を変更したwavファイルの作成 [wave_change_bitdepth.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_change_bitdepth.py)
- 振幅の正規化 [wave_normalize.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_normalize.py)
- ステレオからモノラルに変更 [wave_stereo_to_mono.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_stereo_to_mono.py)
- 白色雑音の作成と書き込み [wave_write_whitenoise.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_write_whitenoise.py)
- wavファイルの再生
  - sounddeviceモジュール [sounddevice_play_wav.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/sounddevice_play_wav.py)
  - subprocessモジュール & 外部再生コマンド [subprocess_play_wav.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/subprocess_play_wav.py)
- wavファイルの録音
  - sounddeviceモジュール；waveモジュールによる音声書き込み [sounddevice_rec_wav.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/sounddevice_rec_wav.py)
  - sounddeviceモジュール；scipyのwavfileモジュールによる音声書き込み [sounddevice_rec_wav_scipy.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/sounddevice_rec_wav_scipy.py)
- 波形プロット
  - matplotlibを利用；waveモジュールによる音声読み込み [plt_waveform.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/plt_waveform.py)
  - matplotlibを利用；scipyのwavfileモジュールによる音声読み込み [plt_waveform_scipy.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/plt_waveform_scipy.py)
  - librosaを利用 [librosa_plot_waveform.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/librosa_plot_waveform.py)
- スペクトログラムのプロット
  - matplotlibを利用 [plt_specgram.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/plt_specgram.py)
  - librosaを利用 [librosa_plot_specgram.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/librosa_plot_specgram.py)
### Jupyter notebook
- wavファイルの再生 [wave_play_wav.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_play_wav.ipynb)
- 波形プロット [plt_waveform.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/WarmUp/plt_waveform.ipynb)
- 波形プロット（librosa利用） [librosa_plot_waveform.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/WarmUp/librosa_plot_waveform.ipynb)
- スペクトログラムのプロット [plt_specgram.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/WarmUp/plt_specgram.ipynb)
- スペクトログラムのプロット（librosa利用） [librosa_plot_specgram.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/WarmUp/librosa_plot_specgram.ipynb)
- 白色雑音のプロットと再生 [plt_whitenoise.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/WarmUp/plt_whitenoise.ipynb)

### Google Colaboratory

音声データはマイドライブ以下、/n-hon-knock/data/ に置くことを前提(in.wav, mono.wav, stereo.wav)

例　"/content/drive/MyDrive/n-hon-knock/data/in.wav"

- wavファイルの読み込みと書き込み
  - waveモジュールによる読み込みと書き込み [wave_read_write.ipynb](https://colab.research.google.com/drive/10M9oW_gRF5Om5NxqbzNAzA-aKNWqmHHu?usp=sharing)
  - scipyのwavfileモジュールによる読み込みと書き込み [wave_read_write_scipy.ipynb](https://colab.research.google.com/drive/17P6IDONQ7cGGZWd0Ld5qIqDs1Gwhx4VI?usp=sharing)
  - soundfileによる読み込みと書き込み [wave_read_write_soundfile.ipynb](https://colab.research.google.com/drive/1APXBY2veqPbVn3gH-hvenGpSCIxejhsl?usp=sharing)
- サンプリング周波数を変更したwavファイルの作成 [wave_change_framerate.ipynb](https://colab.research.google.com/drive/1ilsV-hoSZNTZRktswUzLR92VOMh3XkDa?usp=sharing)
- 量子化ビット数を変更したwavファイルの作成 [wave_change_bitdepth.ipynb](https://colab.research.google.com/drive/1Ck2ebuTR9HNSy9E1mDpq1iPv6gFP02Yg?usp=sharing)
- 振幅の正規化 [wave_normalize.ipynb](https://colab.research.google.com/drive/14JnCsUSzqjgzKAfQ4zGETPxVsSJm1RY2?usp=sharing)
- ステレオからモノラルに変更 [wave_stereo_to_mono.ipynb](https://colab.research.google.com/drive/1SlzadilGSkM-p3Wqpf0cNOr9dO0Y_TBy?usp=sharing)
- 白色雑音の作成と書き込み [wave_write_whitenoise.ipynb](https://colab.research.google.com/drive/1FUiws9cVD7lgx8mN1QKatYxPl7QcM2hX?usp=sharing)
- wavファイルの再生 [wave_play_wav.ipynb](https://colab.research.google.com/drive/1rZQEBuVzbJ2LhTeogAhYTEq1Zb4MFg3w?usp=sharing)
- 波形プロット [plt_waveform.ipynb](https://colab.research.google.com/drive/18hc3xLmpRu5rsJKL6Po9ffUwmTuMftl6?usp=sharing)
- 波形プロット（librosa利用）[librosa_plot_waveform.ipynb](https://colab.research.google.com/drive/1hKSNKo01GtNWPm2m9UOevbp8ECsYntZ-?usp=sharing)
- スペクトログラムのプロット [plt_specgram.ipynb](https://colab.research.google.com/drive/12dHvnmUw0eSlNMihT-ZfrTk6GkygTaNk?usp=sharing)
- スペクトログラムのプロット（librosa利用） [librosa_plot_specgram.ipynb](https://colab.research.google.com/drive/1EH5sQHDGQ8euszV3xXsR6VTPvpc1fUFy?usp=sharing)
