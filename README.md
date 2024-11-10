# ImageRecognitionWinApp

カメラ映像から入力される動画(画像)を、「サトウキビ」「パイナップル」「雑草」に分類し、バウンディングボックスを表示させます。

推論には、[こちら](https://github.com/TechC-SugarCane/ObjectDetection)のリポジトリで作成したモデルを使って行います。

モデルは、YOLOv7とYOLOv10を使用しています。

また、GUIアプリのフレームワークには、CustomTkinterというPythonでGUIアプリが作れるものを使っています。

## TODO

- [x] テスト用動画からの推論方法について記述
- [ ] ドキュメントの作成
- [ ] ユーザーフローの画像のリンク切れを修正

## 画像

### ユーザーフロー

※画像がリンク切れを起こしていますが、画像の所在が不明なので対処できていません。

![ImageRecognitionWinAppUserFlow.png](https://github.com/TechC-SugarCane/ImageRecognitionWinApp/edit/develop/ImageRecognitionWinAppUserFlow.png)

### 画面一覧

![imagerecognitionwinapp_screen.png](https://github.com/TechC-SugarCane/ImageRecognitionWinApp/edit/develop/imagerecognitionwinapp_screen.png)

## Setup

### 1. git-lfsのインストール

テスト用の動画ファイルを扱うために、git-lfsをインストールしてください。

```bash
# mac
brew install git-lfs

# windows
# https://git-lfs.github.com/ からインストーラをダウンロードしてインストール

# git-lfsの初期化
git lfs install
```

### 2. リポジトリをクローン

```bash
git clone git@github.com:TechC-SugarCane/ImageRecognitionWinApp.git

cd ImageRecognitionWinApp
```

### 3. Pythonの環境構築

```bash
pyenv install
```

### 4. 仮想環境を作成

```bash
python -m venv .venv
```

### 5. 仮想環境を有効化

```bash
# mac
source .venv/bin/activate

# windows
.venv\Scripts\activate
```

### 6. ライブラリをインストール

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

# テスト用の動画を使って推論を行う場合
python setup_view.py --test

# serial通信を使って、ノズルから噴出させる場合
python setup_view.py --serial
```

### 3. アプリの操作

1. モデルのバージョンと推論させたい対象を選択
2. 左の開始ボタンを押して、カメラ映像を取得し、推論を開始
※カメラを二台使用する場合は、右の開始ボタンも押してください
3. 推論を停止したい場合は、停止ボタンを押してください

## スクリプトをexe化する

setup_view.pyをexe化して簡単にアプリを起動できるようにすることができます。

```bash
# --noconsoleというオプションは、エラーが出てもわからないため基本おすすめしません
pyinstaller --onefile setup_view.py

# --onefile: 1つのexeファイルにまとめる
```

ビルドが完了すると、`dist/`にexeファイルが生成されます。ただし、モデルのパスの関係上`dist/`で実行するとエラーが出るため、exeファイルはルートディレクトリに移動させてください。<br>
また、exeファイルをコンソール上から実行すれば、通常通り引数を渡すことができます。

```bash
# 例
./setup_view.exe --test
```

## コントリビューター向けガイドライン

コントリビューター向けのガイドラインについては、こちらの[CONTRIBUTING.md](https://github.com/TechC-SugarCane/.github/blob/main/CONTRIBUTING.md)を参照してください。
