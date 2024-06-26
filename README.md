# ImageRecognitionWinApp

カメラ映像から入力される動画(画像)を、「サトウキビ」「パイナップル」「雑草」に分類し、バウンディングボックスを表示させます。

推論には、[こちら](https://github.com/TechC-SugarCane/ObjectDetection)のリポジトリで作成したモデルを使って行います。

モデルは、YOLO v7とNASを使用しています。

また、GUIアプリのフレームワークには、CustomTkinterというPythonでGUIアプリが作れるものを使っています。

## TODO

- [ ] テスト用動画からの推論方法について記述

## 画像

### ユーザーフロー

※画像がリンク切れを起こしていますが、画像の所在が不明なので対処できていません。

![ImageRecognitionWinAppUserFlow.png](https://github.com/TechC-SugarCane/ImageRecognitionWinApp/edit/develop/ImageRecognitionWinAppUserFlow.png)

### 画面一覧

![imagerecognitionwinapp_screen.png](https://github.com/TechC-SugarCane/ImageRecognitionWinApp/edit/develop/imagerecognitionwinapp_screen.png)

## Setup

### 1. リポジトリをクローン

```bash
git clone git@github.com:TechC-SugarCane/ImageRecognitionWinApp.git

cd ImageRecognitionWinApp
```

### 2. Pythonの環境構築

```bash
pyenv install
```

### 3. 仮想環境を作成

```bash
python -m venv .venv
```

### 4. 仮想環境を有効化

```bash
# mac
source .venv/bin/activate

# windows
.venv\Scripts\activate
```

### 5. ライブラリをインストール

```bash
# CPUで推論を行う場合
pip install -r requirements-cpu.txt

# GPUで推論を行う場合
pip install -r requirements-gpu.txt
```

## Usage

### 1. モデルのダウンロード

[こちら](./model/model.md)に従い、すべてのモデルをダウンロードしてください。

その後、`model`ディレクトリにダウンロードしたモデルを配置してください。

### 2. アプリの起動

```bash
python setup_view.py
```

### 3. アプリの操作

1. モデルのバージョンと推論させたい対象を選択
2. 左の開始ボタンを押して、カメラ映像を取得し、推論を開始
※カメラを二台使用する場合は、右の開始ボタンも押してください
3. 推論を停止したい場合は、停止ボタンを押してください
