# 音の電子透かしとステガノグラフィ

## はじめに
音の電子透かしおよびステガノグラフィ技術をPythonで実装するのが目的。

## ファイル一覧
### Pythonスクリプト
- 最下位ビット置換法 [lsb_method.py](https://github.com/tam17aki/speech_process_exercise/blob/master/AudioWatermark/lsb_method.py)
- 拡散スペクトル法 [spread_spectrum_method.py](https://github.com/tam17aki/speech_process_exercise/blob/master/AudioWatermark/spread_spectrum_method.py)
- ケプストラム法 [cepstrum_method.py](https://github.com/tam17aki/speech_process_exercise/blob/master/AudioWatermark/cepstrum_method.py)
- 位相コーディング法 [phase_coding_method.py](https://github.com/tam17aki/speech_process_exercise/blob/master/AudioWatermark/phase_coding_method.py)
- エコーハイディング法 [echo_hiding_method.py](https://github.com/tam17aki/speech_process_exercise/blob/master/AudioWatermark/echo_hiding_method.py)
- ウェーブレット法 [wavelet_method.py](https://github.com/tam17aki/speech_process_exercise/blob/master/AudioWatermark/wavelet_method.py)
- 特異値分解法（STFTに対する）[svd_stft_method.py](https://github.com/tam17aki/speech_process_exercise/blob/master/AudioWatermark/svd_stft_method.py)
- 特異値分解法（複素ケプストラムに対する）[svd_cepstrum method.py](https://github.com/tam17aki/speech_process_exercise/blob/master/AudioWatermark/svd_cepstrum_method.py)
- 特異値分解法（DCT係数に対する）[svd_dct_method.py](https://github.com/tam17aki/speech_process_exercise/blob/master/AudioWatermark/svd_dct_method.py)

### Google Colaboratory
- 最下位ビット置換法 [lsb_method.ipynb](https://colab.research.google.com/drive/1bz8GQZ-IOQ2S7hJELy2xfujzJiddgqeE?usp=sharing)
- 拡散スペクトル法 [spread_spectrum_method.ipynb](https://colab.research.google.com/drive/1yMvfnFOjs2BRsQGhvnypSPyGm4E7DNNq?usp=sharing)
- ケプストラム法 [cepstrum_method.py](https://colab.research.google.com/drive/1IGQXgBiskWaJjhlam8i7m5-ghthsane0?usp=sharing)
