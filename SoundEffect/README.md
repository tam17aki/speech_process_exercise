# 音声加工とサウンドエフェクト
## はじめに
```
brew install sox
pip3 install sox
```

## ファイル一覧
### Pythonスクリプト
#### PySox利用
- wavからrawへ ([pysox_wav2raw.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_wav2raw.py))
- ステレオからモノラルへ ([pysox_stereo2mono.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_stereo2mono.py))
- 量子化ビット数を変更 ([pysox_change_bitdepth.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_change_bitdepth.py))
- サンプリング周波数を変更 ([pysox_change_samplerate.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_change_samplerate.py))
- アップサンプリング（[pysox_upsample.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_upsample.py)）
- ダウンサンプリング（[pysox_downsample.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_downsample.py)）
- エコー ([pysox_echo.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_echo.py))
- リバーブ ([pysox_reverb.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_reverb.py))
- ピッチシフト ([pysox_pitchshift.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_pitchshift.py))
- タイムストレッチ ([pysox_timestretch.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_timestretch.py))
- ローパスフィルタ / ハイパスフィルタ ([pysox_lowpass-highpass.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_lowpass-highpass.py))
- バンドパスフィルタ / バンドリジェクトフィルタ ([pysox_bandpass_bandreject.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_bandpass_bandreject.py))
- トレモロ ([pysox_tremolo.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_tremolo.py))
- フランジャ（[pysox_flanger.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_flanger.py)）

### Jupyter notebook
- エコー [pysox_echo.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_echo.ipynb)
- リバーブ [pysox_reverb.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_reverb.ipynb)
- ピッチシフト [pysox_pitchshift.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_pitchshift.ipynb)
- タイムストレッチ [pysox_timestretch.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_timestretch.ipynb)
- トレモロ [pysox_tremolo.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_tremolo.ipynb)
- 量子化ビット数を変更 [pysox_change_bitdepth.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_change_bitdepth.ipynb)
