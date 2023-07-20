# 話者認識

## はじめに
```
python3 -m pip install librosa
python3 -m pip install hydra-core
python3 -m pip install progressbar2
python3 -m pip install torch
python3 -m pip install torchaudio
python3 -m pip install xvector-jtubespeech
```
## 使用データ
- [in.wav](https://drive.google.com/file/d/1lsN-is31x_snFBTNGR05pQwX9RhzC8sb/view?usp=sharing)
- [config.yaml](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeakerRecognition/config.yaml)
- [声優統計コーパス](https://voice-statistics.github.io/)

## ファイル一覧
- xvectorの抽出 via xvector-jtubespeech
  - 抽出のお試し
  - 声優統計コーパス
    - コーパスのダウンロード [download_voicestats_corpus.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeakerRecognition/download_voicestats_corpus.py)
    - 事前学習済モデルのダウンロード [download_pretrained_model.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeakerRecognition/download_pretrained_model.py)
    - xvectorを抽出して保存 [extract_xvector_voicestats.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeakerRecognition/extract_xvector_voicestats.py)
   
- 話者認識モデルを動かす
  - 声優統計コーパス   
    - サポートベクトルマシン
    - フィードフォワードニューラルネット (PyTorch) [spk_recog_mlp.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeakerRecognition/spk_recog_mlp.py)
