# 第1章 準備運動（音声読み込み・書き込みなど）
## はじめに
```
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
pip3 install sounddevice
```

## ファイル一覧
- wavファイルの読み込みと書き込み
  - waveモジュールによる読み込みと書き込み [wave_read_write.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_read_write.py)
  - scipyのwavfileモジュールによる読み込みと書き込み [wave_read_write_scipy.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_read_write_scipy.py)
- サンプリング周波数を変更したwavファイルの作成 
  - [wave_change_framerate.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_change_framerate.py)
- 量子化ビット数を変更したwavファイルの作成
  - [wave_change_bitdepth.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_change_bitdepth.py)
- 振幅の正規化
  - [wave_normalize.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_normalize.py)
- ステレオからモノラルに変更
  - [wave_stereo_to_mono.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_stereo_to_mono.py)
- 白色雑音の作成と書き込み
  - [wave_write_whitenoise.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/wave_write_whitenoise.py)
- wavファイルの再生
  - sounddeviceモジュール [sounddevice_play_wav.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/sounddevice_play_wav.py)
  - subprocessモジュール & 外部再生コマンド [subprocess_play_wav.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/subprocess_play_wav.py)
- 波形プロット
  - matplotlibを利用；waveモジュールによる音声読み込み [plt_waveform.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/plt_waveform.py)
  - matplotlibを利用；scipyのwavfileモジュールによる音声読み込み [plt_waveform_scipy.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/plt_waveform_scipy.py)
  - librosaを利用 [librosa_plot_waveform.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/librosa_plot_waveform.py)
- スペクトログラムのプロット
  - matplotlibを利用 [plt_specgram.py](https://github.com/tam17aki/speech_process_exercise/blob/master/WarmUp/plt_specgram.py)
