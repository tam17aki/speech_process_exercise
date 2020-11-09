# ディジタル信号処理の基礎
## ファイル一覧
### Pythonスクリプト
- 正弦波の作成 ([dsp_sine.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_sine.py)) と プロット ([dsp_sine_plot.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_sine_plot.py))
  - うなりが発生する正弦波の作成 ([dsp_sine_beat.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_sine_beat.py))
  - 雑音を重畳した正弦波の作成 ([dsp_sine_addnoise.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_sine_addnoise.py)) と プロット ([dsp_sine_addnoise_plot.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_sine_addnoise_plot.py))
- 複素正弦波の作成とプロット ([dsp_sine_euler.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_sine_euler.py))
- 矩形波、ノコギリ波、三角波の作成とプロット
- フーリエ級数展開（矩形波、ノコギリ波、三角波の合成）
  - 矩形波の合成 ([dsp_rectangle_fourier.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_rectangle_fourier.py))
  - ノコギリ波の合成 ([dsp_sawtooth_fourier.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_sawtooth_fourier.py))
  - 三角波の合成 ([dsp_triangle_fourier.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_triangle_fourier.py))
- 離散時間フーリエ変換
- インパルス信号の作成とプロット
- 窓関数の作成とプロット
  - Hann窓 ([dsp_window_hann.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_window_hann.py))
  - Hamming窓 ([dsp_window_hamming.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_window_hamming.py))
  - Blackman窓 ([dsp_window_blackman.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_window_blackman.py))
- FIRフィルタ
  - 畳み込み (線形時不変システム的な意味で)
  - 移動平均フィルタによるノイズ除去 ([dsp_fir_denoise.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_fir_denoise.py))
  - ローパスフィルタ、ハイパスフィルタ
- 自己相関、相互相関
- Z変換、逆Z変換
- ヒルベルト変換による包絡線の抽出と波形再合成 ([dsp_hilbert.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_hilbert.py))
- おまけ（フーリエ級数近似のアニメーション作成）
  - 矩形波 ([dsp_rectangle_anime.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_rectangle_anime.py))、アニメーション ([rectangle_anime.mp4](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/rectangle_anime.mp4)) 
  - ノコギリ波 ([dsp_sawtooth_anime.py](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_sawtooth_anime.py))、アニメーション ([sawtooth_anime.mp4](https://github.com/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/sawtooth_anime.mp4)) 

### Jupyter notebook
- 正弦波の作成 ([dsp_sine.ipynb](https://nbviewer.jupyter.org/github/tam17aki/speech_process_exercise/blob/master/DigitalSignalProcessing/dsp_sine.ipynb))
