# RT-F-HACKATHON/teamF_app

RareTECH 2023 年秋 Hackathon F チームの ChatApp です。

**起動方法**

```
docker compose up
```

### ディレクトリ構成

```

├── ChatApp              # サンプルアプリ用ディレクトリ
│   ├── __init__.py     # ディレクトリをパッケージして扱う初期化ファイル
│   ├── app.py          # アプリケーションプログラム
│   ├── models.py       # SQL実施関数プログラム
│   ├── static          # 静的ファイル用ディレクトリ
│   ├── templates       # Template(HTML)用ディレクトリ
│   ├── util            # データベース接続プログラム
│   └── uwsgi.ini       # uwsgi用の初期設定ファイル
├── Docker
│   ├── Flask
│   │   └── Dockerfile # Flask(Python)用Dockerファイル
│   └── MySQL
│   │  ├── Dockerfile  # MySQL用Dockerファイル
│   │  ├── init.sql    # MySQL初期設定ファイル
│   │  └── my.cnf      # MySQL基本設定ファイル
│   └── nginx
│       ├── Dockerfile  # nginx用Dockerファイル
│       └── nginx.conf  # nginx用設定ファイル
├── docker-compose.yml   # Docker-composeファイル
├── docker-compose-dep.yml # AWSデプロイ時使用Docker-composeファイル
└── requirements.txt     # 使用モジュール記述ファイル
```
