# テスト動画について

- 推論のテストに使用する動画は、以下のリンクからダウンロードしてください。
- ダウンロードしたフォルダは、`tests` ディレクトリに配置してください。

## ダウンロードリンク

この中にあるフォルダごとダウンロードしてください。

- [テスト動画 | sharepoint](https://jikeigroupcom.sharepoint.com/:f:/s/msteams_04e6ef/EtHm-lo3gw5JmedevdS-yHABLzIi1-pK5Czs7t5nzb2j5A?e=QvPZCE)

ダウンロードしたら、[#フォルダ構成](#フォルダ構成)を参考に、`video/tests`にフォルダを配置してください。

## フォルダ構成

```plaintext
video
├── README.md
├── tests/
│   ├── sugarcane/
│   │   ├── xxx.mp4
│   │   └── yyy.mp4
│   └── pineapple/
│       ├── xxx.mp4
│       └── yyy.mp4
```

## 外部リンクからダウンロードすることになった経緯

- GitHub のlfsストレージの容量制限により、リポジトリ内に動画を配置することができなくなりました。
  - リモートリポジトリのlfs objectを削除する事ができないため
  - lfs objectを削除するためには、リモートリポジトリを削除して再度作成する必要がある、つまりPRやissueが履歴もろとも削除されるため、現状は避けるべきと判断しました。
- そのため、動画ファイルを外部リンクからダウンロードする形に変更しました。
