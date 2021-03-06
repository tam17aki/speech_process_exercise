# 第4章 音声の特徴量抽出

## はじめに
```
pip3 install librosa
pip3 install pysptk
pip3 install pyworld
```

## ファイル一覧
### Pythonスクリプト
- 短時間フーリエ変換（stft）
- 逆短時間フーリエ変換（istft; オーバーラップ加算）
- 音声の短時間フーリエ変換と逆短時間フーリエ変換（scipy利用）
  - stftした直後にistftして音声を復元する [feat_stft_istft.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_stft_istft.py)
- スペクトログラム
  - stftした後に振幅スペクトルを計算 [feat_stft_spec.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_stft_spec.py)
- 位相復元（Griffin-Limアルゴリズム）
  - オリジナル [feat_gla.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_gla.py)
  - Masuyama氏らが提案したADMMに基づく高速版アルゴリズム [feat_gla_admm.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_gla_admm.py)
- メルスペクトログラム
  - librosa利用 [feat_melspec.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_melspec.py)
- MFCC
  - librosa利用 [feat_mfcc.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_mfcc.py)
- ケプストラム、メルケプストラム
- 線形予測係数
  - PySPTK利用
  - librosa利用
- PARCOR係数
- LSP係数
- 基本周波数の抽出
  - YINアルゴリズム [feat_fo_yin.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_yin.py)
  - probabilistic YINアルゴリズム [feat_fo_pyin.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_pyin.py)
  - 自己相関法 [feat_fo_autocorr.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_autocorr.py)
  - 変形自己相関法 [feat_fo_autocorr_variant.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_autocorr_variant.py)
  - ケプストラム法 [feat_fo_cepstrum.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_cepstrum.py)
  - DIOアルゴリズム [feat_fo_dio.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_dio.py)
### Jupyter notebook
- スペクトログラム の抽出
  - [feat_stft_spec.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_stft_spec.ipynb)
- メルスペクトログラムの抽出
  - [feat_melspec.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_melspec.ipynb)
- MFCCの抽出
  - [feat_mfcc.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_mfcc.ipynb)
- 基本周波数の抽出
  - YINアルゴリズム [feat_fo_yin.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_yin.ipynb)
  - probabilistic YINアルゴリズム [feat_fo_pyin.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_pyin.ipynb)
  - 自己相関法 [feat_fo_autocorr.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_autocorr.ipynb)
  - 変形自己相関法 [feat_fo_autocorr_variant.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_autocorr_variant.ipynb)
  - ケプストラム法 [feat_fo_cepstrum.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_cepstrum.ipynb)
  - DIOアルゴリズム [feat_fo_dio.ipynb](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_dio.ipynb)
