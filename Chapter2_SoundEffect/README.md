# 第２章 音声加工とサウンドエフェクト
## はじめに
```
brew install sox
pip3 install sox
```

## ファイル一覧
### SoXのみ(without Python)
- comming soon...
### Pythonのみ (without PySoX)
- coming soon...
### PySoXを用いた音声加工（サウンドエフェクト処理）
- wavからrawへ ([pysox_wav2raw.py](https://github.com/tam17aki/speech_process_exercise/blob/master/Chapter2_SoundEffect/pysox_wav2raw.py))
- ステレオからモノラルへ ([pysox_stereo2mono.py](https://github.com/tam17aki/speech_process_exercise/blob/master/Chapter2_SoundEffect/pysox_stereo2mono.py))
- 量子化ビット数を変更 ([pysox_change_bitdepth.py](https://github.com/tam17aki/speech_process_exercise/blob/master/Chapter2_SoundEffect/pysox_change_bitdepth.py))
- サンプリング周波数を変更 ([pysox_change_samplerate.py](https://github.com/tam17aki/speech_process_exercise/blob/master/Chapter2_SoundEffect/pysox_samplerate.py))
- エコー ([pysox_echo.py](https://github.com/tam17aki/speech_process_exercise/blob/master/Chapter2_SoundEffect/pysox_echo.py))
- リバーブ ([pysox_reverb.py](https://github.com/tam17aki/speech_process_exercise/blob/master/Chapter2_SoundEffect/pysox_reverb.py))
- ピッチシフト ([pysox_pitchshift.py](https://github.com/tam17aki/speech_process_exercise/blob/master/Chapter2_SoundEffect/pysox_pitchshift.py))
- タイムストレッチ ([pysox_timestretch.py](https://github.com/tam17aki/speech_process_exercise/blob/master/Chapter2_SoundEffect/pysox_timestretch.py))
- ローパスフィルタ / ハイパスフィルタ ([pysox_lowpass-highpass.py](https://github.com/tam17aki/speech_process_exercise/blob/master/Chapter2_SoundEffect/pysox_lowpass-highpass.py))
- バンドパスフィルタ / バンドリジェクトフィルタ ([pysox_bandpass_bandreject.py](https://github.com/tam17aki/speech_process_exercise/blob/master/Chapter2_SoundEffect/pysox_bandpass_bandreject.py))
- トレモロ ([pysox_tremolo.py](https://github.com/tam17aki/speech_process_exercise/blob/master/Chapter2_SoundEffect/pysox_tremolo.py))
