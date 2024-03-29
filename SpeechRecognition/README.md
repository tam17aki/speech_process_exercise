# 音声認識

## はじめに
```
pip3 install pysimplegui
pip3 install sounddevice
pip3 install soundfile
pip3 install SpeechRecognition
pip3 install gtts
pip3 install wikipedia
pip3 install vosk
```

## ファイル一覧
- 指定秒数だけ音声（wav）を録音 with soundfile & sounddevice ([record_speech.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechRecognition/record_speech.py))
- 収録済み音声（wav）に対する音声認識 with VOSK ([vosk_asr_recorded.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechRecognition/vosk_asr_recorded.py))
- マイク音声入力によるストリーミング音声認識 with VOSK ([vosk_asr_streaming.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechRecognition/vosk_asr_streaming.py))
- マイク音声入力によるVADつきストリーミング音声認識 with VOSK ([vosk_asr_streaming_vad.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechRecognition/vosk_asr_streaming_vad.py))

### PySimpleGUIによるGUIアプリ
- 指定秒数だけ音声を録音し、音声認識をかける with SpeechRecognition ([recog_speech_rec.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechRecognition/recog_speech_rec.py))
- Google Homeもどき ([google_mode_modoki.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechRecognition/google_mode_modoki.py))
- 音声認識結果を使ったWikipedia検索＆読み上げ ([recog_wikipedia.py](https://github.com/tam17aki/speech_process_exercise/blob/master/SpeechRecognition/recog_wikipedia.py))

### Google Colaboratory
- Juliusの日本語ディクテーションキット ([Link](https://colab.research.google.com/drive/1pdp9lmzzslLzN95iu69siTkTxMk-hzXf?usp=sharing))
- SpeechRecognition ライブラリのデモンストレーション ([Link](https://colab.research.google.com/drive/1w96tb5SxCPWqnNXaVlFQpaMPzJ24w0F3?usp=sharing)) 
- ESPnet2　事前学習済モデルを用いた音声認識デモンストレーション
  - LaboroTVSpeechコーパス ([Link](https://colab.research.google.com/drive/1xJ96-7JSSPBNJ-bAwysESDcaGvnbblAR?usp=sharing))
- VOSK ライブラリを用いた音声認識デモンストレーション ([Link](https://colab.research.google.com/drive/1Dvhw4H2hT3WxDniX2M8w7q1pae5qgXYy?usp=sharing))
