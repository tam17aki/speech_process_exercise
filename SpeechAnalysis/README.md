# 音声の特徴量抽出

## はじめに
```
pip3 install librosa
pip3 install pysptk
pip3 install pyworld
```

## 使用データ
以下からダウンロード
- [in.wav](https://drive.google.com/file/d/1lsN-is31x_snFBTNGR05pQwX9RhzC8sb/view?usp=sharing)

## ファイル一覧
### Pythonスクリプト
- 短時間フーリエ変換（stft）
  - scipy利用 [feat_stft.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_stft.py)
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
- ケプストラム
  - リフタリングによりスペクトル包絡を抽出 [feat_cepstrum.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_cepstrum.py)
- メルケプストラム
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
  - [feat_stft_spec.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_stft_spec.ipynb)
- メルスペクトログラムの抽出
  - [feat_melspec.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_melspec.ipynb)
- 位相復元（Griffin-Limアルゴリズム）
  - オリジナル [feat_gla.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_gla.ipynb)
  - Fast Griffin-Limアルゴリズム （librosa） [feat_librosa_gla.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_librosa_gla.ipynb)
  - Masuyama氏らが提案したADMMに基づく高速版アルゴリズム [feat_gla_admm.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_gla_admm.ipynb)
- MFCCの抽出
  - [feat_mfcc.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_mfcc.ipynb)
- 基本周波数の抽出
  - YINアルゴリズム [feat_fo_yin.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_yin.ipynb)
  - probabilistic YINアルゴリズム [feat_fo_pyin.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_pyin.ipynb)
  - 自己相関法 [feat_fo_autocorr.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_autocorr.ipynb)
  - 変形自己相関法 [feat_fo_autocorr_variant.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_autocorr_variant.ipynb)
  - ケプストラム法 [feat_fo_cepstrum.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_cepstrum.ipynb)
  - DIOアルゴリズム [feat_fo_dio.ipynb](https://nbviewer.org/github/tam17aki/speech_process_exercise/blob/master/SpeechAnalysis/feat_fo_dio.ipynb)

### Google Colaboratory
- Scipyによる短時間フーリエ変換の計算およびスペクトログラムのプロット [feat_stft_spec.ipynb](https://colab.research.google.com/drive/1I6SrsgqwLfZItSAapMWzb-90lNLJWBZS?usp=sharing)
- メルスペクトログラムの抽出の可視化 [feat_melspec.ipynb](https://colab.research.google.com/drive/1B2pCOHnYpQ58-7WClpUxac6EPnRIO0Kh?usp=sharing)
- 線形予測係数の抽出
  - PySPTK利用 [feat_lpc.ipynb](https://colab.research.google.com/drive/1UkcgpdQWhqOm7spf6iqIyR-3ooLrXVQp?usp=sharing)
- PARCOR係数の抽出 [feat_parcor.ipynb](https://colab.research.google.com/drive/1AUQ2y_I0f8hTzQY0d2ZpZkfsi-15-Cpz?usp=sharing)
- 線スペクトル対の抽出 [feat_lsp.ipynb](https://colab.research.google.com/drive/1M4NEMCyosNnnexEZmfOqrjcykZF6SbJU?usp=sharing)
- ケプストラムの抽出
  - 全フレーム対象 [feat_cepstrum.ipynb](https://colab.research.google.com/drive/15EInBrNJ7REUJ1i5N0VUuL0RXC5nLZ-t?usp=sharing)
  - パワー最大のフレームに対してケプストラム抽出 & スペクトル包絡抽出 [feat_cepstrum_envelop.ipynb](https://colab.research.google.com/drive/1mt0lyDlp_UEcRjCBmacMPcW5rqxH-gFG?usp=sharing)
- メルケプストラムの抽出
  - 全フレーム対象 [feat_mcep.ipynb](https://colab.research.google.com/drive/1S97-ZIWyfCGJHryFnYMib22EPH7ImPAG?usp=sharing)
- スペクトル包絡の抽出
  - PySPTK利用 [feat_plot_envelops_pysptk.ipynb](https://colab.research.google.com/drive/1jcyS0NFXyeRFbgsKwsyoMiSpJyz3yM8O?usp=sharing)
  - PyWORLD利用 [feat_envelop_pyworld.ipynb](https://colab.research.google.com/drive/12IdRb8m20hQ0BBUuwQ1FG35K49rmwPsR?usp=sharing)
- MFCCの抽出 [feat_mfcc.ipynb](https://colab.research.google.com/drive/1e-ujQqrWe0xNr-Adq6EQkFyO2YtmuWYr?usp=sharing)
- 基本周波数の抽出
  - RAPTアルゴリズム [feat_fo_rapt.ipynb](https://colab.research.google.com/drive/17RLdZ9v9sgvjFRwnI_3LvnrSxMXsBDao?usp=sharing)
  - SWIPE'アルゴリズム [feat_fo_swipe.ipynb](https://colab.research.google.com/drive/1j7y7abQwOuu9abhIts_jWhMyBEkUh8oa?usp=sharing)
  - YINアルゴリズム [feat_fo_yin.ipynb](https://colab.research.google.com/drive/1DuhkR82bHLJibmr5IDFP2-8qUIUDpj9P?usp=sharing)
  - probabilistic YINアルゴリズム [feat_fo_pyin.ipynb](https://colab.research.google.com/drive/10XZvN6V7BZLNwextRxBrpNmpwUnbzR9T?usp=sharing)
  - DIOアルゴリズム [feat_fo_dio.ipynb](https://colab.research.google.com/drive/1AGfo-DcMdPGmA5903Ffhl6QzALn8AFhR?usp=sharing)
- 位相復元
  - Masuyama氏らが提案したADMMに基づく高速位相復元アルゴリズム [feat_gla_admm.ipynb](https://colab.research.google.com/drive/1zUkhSgUgxmxBzjJZBwnRcz9yXvxxNDZT?usp=sharing)
