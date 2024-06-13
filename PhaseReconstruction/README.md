# 位相復元

## はじめに

```
pip3 install numpy
pip3 install soundfile
pip3 install oct2py
pip3 install scipy
```

OctPy経由でMATLAB/GNU Octave用ライブラリLTFATとPHASERETを利用し，音声の位相復元を実装する．

事前にOctaveのインストールを済ませておく．

1. GitHubからltfatの[最新版](https://github.com/ltfat/ltfat)をダウンロードし，適切な場所で解凍する．

   例えばパスは /home/hoge/ltfat-main とする
   
2. GitHubからphaseretの[最新版](https://github.com/ltfat/phaseret)をダウンロードし， ltfat-main直下に解凍する．

   例えばパスは /home/hoge/ltfat-main/phaseret-main とする
   
3. ltfat-mainに移動して octave を起動し，

   ```
   octave> ltfatstart;
   octave> ltfatmex;
   ```
   によって事前にライブラリのコンパイルを済ませておく（'octave>' はプロンプト）．
   
   octave上からphaseret-mainに移動して，同様にコンパイルを済ませておく．

   ```
   octave> phaseretstart;
   octave> phaseretmex;
   ```

### Pythonスクリプト
