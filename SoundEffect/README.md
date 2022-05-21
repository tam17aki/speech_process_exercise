# 音声加工とサウンドエフェクト
## はじめに
```
brew install sox
pip3 install sox
```

## 使用データ
以下からダウンロード
- [in.wav](https://drive.google.com/file/d/1lsN-is31x_snFBTNGR05pQwX9RhzC8sb/view?usp=sharing)
- [mono.wav](https://drive.google.com/file/d/1_nKAtHg4qsY0HMdLxrYsVywqDqdjY9GA/view?usp=sharing)
- [stereo.wav](https://drive.google.com/file/d/1V1Uwb1UAD51ouy9t0B89lWsDjErFPSpZ/view?usp=sharing)

## ファイル一覧
### Pythonスクリプト
#### PySox利用
- wavからrawへ [pysox_wav2raw.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_wav2raw.py)
- ステレオからモノラルへ [pysox_stereo2mono.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_stereo2mono.py)
- 量子化ビット数を変更 [pysox_change_bitdepth.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_change_bitdepth.py)
- サンプリング周波数を変更 [pysox_change_samplerate.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_change_samplerate.py)
- アップサンプリング [pysox_upsample.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_upsample.py)
- ダウンサンプリング [pysox_downsample.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_downsample.py)
- エコー [pysox_echo.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_echo.py)
- リバーブ [pysox_reverb.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_reverb.py)
- ピッチシフト [pysox_pitchshift.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_pitchshift.py)
- タイムストレッチ [pysox_timestretch.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_timestretch.py)
- ローパスフィルタ / ハイパスフィルタ [pysox_lowpass-highpass.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_lowpasshighpass.py)
- バンドパスフィルタ / バンドリジェクトフィルタ [pysox_bandpass_bandreject.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_bandpass_bandreject.py)
- トレモロ [pysox_tremolo.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_tremolo.py)
- フランジャ [pysox_flanger.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_flanger.py)

### Jupyter notebook
- エコー [pysox_echo.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_echo.ipynb)
- リバーブ [pysox_reverb.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_reverb.ipynb)
- ピッチシフト [pysox_pitchshift.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_pitchshift.ipynb)
- タイムストレッチ [pysox_timestretch.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_timestretch.ipynb)
- トレモロ [pysox_tremolo.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_tremolo.ipynb)
- 量子化ビット数を変更 [pysox_change_bitdepth.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/SoundEffect/pysox_change_bitdepth.ipynb)

### Google Colaboratory
音声データはマイドライブ以下、/n-hon-knock/data/ に置くことを前提(in.wav, mono.wav, stereo.wav)

例　"/content/drive/MyDrive/n-hon-knock/data/in.wav"

- wavからrawへ [pysox_wav2raw.ipynb](https://colab.research.google.com/drive/1VeuLRCsv7rjF9Hj_nALpx0FRTAYl5-I7?usp=sharing)
- ステレオからモノラルへ [pysox_stereo2mono.ipynb](https://colab.research.google.com/drive/1PBBO7C6zaDtqEwgW0obD7j2WoQE2O-n7?usp=sharing)
- 量子化ビット数を変更 [pysox_change_bitdepth.ipynb](https://colab.research.google.com/drive/1jq2lLLjO5PHHx2GOTGomUNxcsEwbHDuJ?usp=sharing)
- サンプリング周波数を変更 [pysox_change_samplerate.ipynb](https://colab.research.google.com/drive/1_UzkR_bErXOGGsJOgIzqNDNBaRycMYwe?usp=sharing)
- アップサンプリング [pysox_upsample.ipynb](https://colab.research.google.com/drive/1oXQX9ye9hAR3BfIZdCq4z79745RhL0hC?usp=sharing)
- ダウンサンプリング [pysox_downsample.ipynb](https://colab.research.google.com/drive/1JUmtoIS3kMWfk5kA3zq8Sd2Q_P1qTlU-?usp=sharing)
- エコー [pysox_echo.ipynb](https://colab.research.google.com/drive/1ZbagzzEtmxBflNtkg_CHlpqsvvmmnhFp?usp=sharing)
- リバーブ [pysox_reverb.ipynb](https://colab.research.google.com/drive/1oNbo4K9wJqcN0pf1rC0_augjx0MbdH4e?usp=sharing)
- ピッチシフト [pysox_pitchshift.ipynb](https://colab.research.google.com/drive/1BszUSRu2M8oktHUGDU5PkOnyGT2zq6Ch?usp=sharing)
- タイムストレッチ [pysox_timestretch.ipynb](https://colab.research.google.com/drive/1x1YcwumqFpub8nl-xj0uiGW0NyWKfCT_?usp=sharing)
- トレモロ [pysox_tremolo.ipynb](https://colab.research.google.com/drive/1gK0TErg9pKt7pBN4Nkd5Fxoo4ubdedwS?usp=sharing)
- フランジャ [pysox_flanger.ipynb](https://colab.research.google.com/drive/10ZuyPjwzYMKZfZlpWVkqcvFXXti6J4Sd?usp=sharing)
- ローパス・ハイパス・バンドパス・バンドリジェクトフィルタ [pysox_filters.ipynb](https://colab.research.google.com/drive/1zO7Y5yKASoit_9q2JKIIldV2aCDJJL8H?usp=sharing)
