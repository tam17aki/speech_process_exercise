# 音源分離
## はじめに
```
pip3 install pyroomacoustics
pip3 install nussl
```

- pyroomacoustics https://github.com/LCAV/pyroomacoustics
- nussl https://github.com/nussl/nussl

### Pythonスクリプト
- pyroomacoustics
  - ILRMAベースの音源分離 [pra_ILRMA.py](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/AudioSourceSeparation/pra_ILRMA.py)

### Jupyter notebook
- pyroomacoustics
  - ILRMAベースの音源分離 [pra_ILRMA.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/AudioSourceSeparation/pra_ILRMA.ipynb)


### Google Colaboratory
- nussl
  - AudioSignal入門 [Introduction_to_AudioSignal.ipynb](https://colab.research.google.com/drive/1ntYryCmSam1El-WWIWRzYS8a9f8Fa8d5?usp=sharing)
  - STFT表現 [audio_signal_stft.ipynb](https://colab.research.google.com/drive/1ALGz70yCLTn1y6njR4D9DCr5qNIku_la?usp=sharing)
  - 周波数マスキング入門 [masking_audio_signal_timefreq.ipynb](https://colab.research.google.com/drive/1qPyDcUAOwsfDZ_X1x_yn1Zqb2Ef52QUr?usp=sharing)
  - ローパス・ハイパスフィルタによる音源分離 [high-lowpass_filters.ipynb](https://colab.research.google.com/drive/1tTqqcBgWFK0wGQeZZjJXUGE9_4ja2GM2?usp=sharing)
  - 理想バイナリマスクによる音源分離 [ideal_binary_mask.ipynb](https://colab.research.google.com/drive/1sxQu62bunrIcjslTl01HGmwyPdjTM4i4?usp=sharing)
  - 理想 ratio マスク（ソフトマスク）による音源分離 [ideal_mask.ipynb](https://colab.research.google.com/drive/1XYMJqc6X_9vKptt5irrGTi-deLoMGwF8?usp=sharing)
  - ウィーナーフィルタによる信号復元（音源分離結果の強調） [wiener_filter.ipynb](https://colab.research.google.com/drive/1f6fbPZNAG8iO2bgZFyFOlAGPiwx7CTr9?usp=sharing)
  - ロバストPCAによる音源分離（歌声と楽曲の分離）[robust_pca.ipynb](https://colab.research.google.com/drive/1S34MIYs-_OCKEt7YULR2MfJpJ_TaOUVx?usp=sharing)
  - 独立成分分析による音源分離 [ica.ipynb](https://colab.research.google.com/drive/1q3Pk5EXMS3GXO0kRkms5mxIzbfw0o3dQ?usp=sharing)
  - 2次元フーリエ変換による音源分離（歌声と楽曲の分離）[2-d_fourier.ipynb](https://colab.research.google.com/drive/1G6c8SLP6bpnu_3f_AaAk2nK4FgzoSbC8?usp=sharing)
  - REPET法による音源分離（歌声と楽曲の分離）[REPET.ipynb](https://colab.research.google.com/drive/1H4IcYHJSD2F9XBjrCNoGtrMjmrg7Up9W?usp=sharing)
  - REPET-SIM法による音源分離（歌声と楽曲の分離）[REPETSIM.ipynb](https://colab.research.google.com/drive/12X9Pvv94vcDIQlv1pUYNqt_HsJCVhiWw?usp=sharing)
  - Timber clusteringによる音源分離 [timber_clustering.ipynb](https://colab.research.google.com/drive/1f8sFW6TJaCvyi7YL9tvg-TgTUnBi2Bu_?usp=sharing)
  - 調波打楽器音分離 [hpss.ipynb](https://colab.research.google.com/drive/1UKrPpfTMSmDxEOcX5xiqxUXn-ElvD-vB?usp=sharing)
  - 空間クラスタリングによる音源分離 [spatial_clustering.ipynb](https://colab.research.google.com/drive/1gYfOZqvtoGL0W00XA-f6Ro16qNev79Dt?usp=sharing)
  - PROJET法による音源分離 [PROJET.ipynb](https://colab.research.google.com/drive/15gs2AFfh3Pj60r_Vn21O8-MmXBXL_07x?usp=sharing)
  - DUET法によるによるブラインド音源分離 [DUET.ipynb](https://colab.research.google.com/drive/15BEzg7TWd4yoiTN5nx-5Xh82Mysczkfh?usp=sharing)
