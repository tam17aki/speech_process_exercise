# 第4章 音声の特徴量抽出

## はじめに
```
pip3 install librosa
pip3 install pysptk
```

## ファイル一覧
- 音声のフレーム分割と窓掛け
  - librosaとPySPTK利用
- 短時間フーリエ変換（stft）
- 逆短時間フーリエ変換（istft; オーバーラップ加算）
- 音声の短時間フーリエ変換と逆短時間フーリエ変換（scipy利用）
  - stftした直後にistftして音声を復元する [feat_stft_istft.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_stft_istft.py)
- スペクトログラム
- 位相復元（Griffin-Limアルゴリズム）
  - オリジナル [feat_gla.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_gla.py)
  - Masuyama氏らが提案したADMMに基づく高速版アルゴリズム [feat_admm_gla.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_admm_gla.py)
- メルスペクトログラム
  - librosa利用 [feat_melspec.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_melspec.py)
- MFCC
  - PySPTK利用
  - librosa利用
- ケプストラム、メルケプストラム
- LPC係数
  - PySPTK利用
  - librosa利用
- PARCOR係数
- LSP係数
- 基本周波数の抽出
  - YINアルゴリズム [feat_fo_yin.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_yin.py)
  - probabilistic YINアルゴリズム [feat_fo_pyin.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_pyin.py)
  - 自己相関法 [feat_fo_autocorr.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_autocorr.py)
  - ケプストラム法 [feat_fo_cepstrum.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_cepstrum.py)
