# ImageRecognitionWinApp

カメラ映像から入力される動画(画像)を、「サトウキビ」「パイナップル」「雑草」に分類し、バウンディングボックスを表示させます。

推論には、下記リポジトリで作成したモデルを使って行います。

- [YOLOv7](https://github.com/TechC-SugarCane/train-YOLOv7)
- [YOLOv9](https://github.com/TechC-SugarCane/train-YOLOv9)
- [YOLOv10](https://github.com/TechC-SugarCane/train-YOLOv10)

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
# Windows
pyenv install


# Macの場合はちょっと特殊
brew install tcl-tk

echo 'tkinterPath="/opt/homebrew/opt/tcl-tk"' >> ~/.zshrc
echo 'export PATH="$tkinterPath/bin:$PATH"' >> ~/.zshrc
echo 'export LDFLAGS="-L$tkinterPath/lib"' >> ~/.zshrc
echo 'export CPPFLAGS="-I$tkinterPath/include"' >> ~/.zshrc
echo 'export PKG_CONFIG_PATH="$tkinterPath/lib/pkgconfig"' >> ~/.zshrc

source ~/.zshrc
pyenv install
# shellの再起動
exec $SHELL -l
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

[models/README.md](./models/README.md)に従い、すべてのモデルをダウンロードしてください。

### 2. アプリの起動

```bash
python setup_view.py
```

#### テスト用動画のランダムを固定する

テスト動画が複数ある時を見据えて、`video/tests/{crop_type}/`にある動画をランダムで選択するようになっています。そのため、テスト動画を固定したい場合は、`--video_seed`オプションを指定してください。

```bash
python setup_view.py --video_seed 0
# or
python setup_view.py -s 0
```

### 3. アプリの操作

1. モデルのバージョンと推論させたい対象を選択
   - テストモード: カメラを使わず動画で推論テストを行う
   - シリアル通信モード: シリアル通信を使用してハードウェアと連携させる
2. 左の開始ボタンを押して、カメラ映像を取得し、推論を開始
    - ※カメラを二台使用する場合は、右の開始ボタンも押してください
3. 推論を停止したい場合は、停止ボタンを押してください

## スクリプトをexe化する

setup_view.pyをexe化して簡単にアプリを起動できるようにすることができます。

```bash
# --noconsoleというオプションは、エラーが出てもわからないため基本おすすめしません
pyinstaller --onefile setup_view.py

# --onefile: 1つのexeファイルにまとめる
```

ビルドが完了すると、`dist/`にexeファイルが生成されます。ただし、モデルのパスの関係上`dist/`で実行するとエラーが出るため、exeファイルはルートディレクトリに移動させてください。<br>

## コントリビューター向けガイドライン

コントリビューター向けのガイドラインについては、こちらの[CONTRIBUTING.md](https://github.com/TechC-SugarCane/.github/blob/main/CONTRIBUTING.md)を参照してください。

### PRを出す時

Pythonファイルが含まれた実装PRは[lintのCI](./.github/workflows/lint.yml)が走るようになっています。

PRを出す前に、下記コマンドでlintを実行し、エラーが出たら修正してください。

#### linter

```bash
# lint
ruff check .
# lintの修正コマンド
ruff check . --fix
```

#### formatter

```bash
ruff format .
```

#### type check

```bash
mypy --ignore-missing-imports --explicit-package-bases .
```
