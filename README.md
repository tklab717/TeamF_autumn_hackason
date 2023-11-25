# RT-F-HACKATHON/teamF_app

RareTECH 2023 年秋 Hackathon F チームの ChatApp です。

**起動方法**

```
docker compose up
```

### ディレクトリ構成

```

├── ChatApp              # サンプルアプリ用ディレクトリ
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── static          # 静的ファイル用ディレクトリ
│   ├── templates       # Template(HTML)用ディレクトリ
│   ├── util
│   └── uwsgi.ini       # uwsgi用の初期設定ファイル
├── Docker
│   ├── Flask
│   │   └── Dockerfile # Flask(Python)用Dockerファイル
│   └── MySQL
│   │  ├── Dockerfile  # MySQL用Dockerファイル
│   │  ├── init.sql    # MySQL初期設定ファイル
│   │  └── my.cnf
│   └── nginx
│       ├── Dockerfile  # nginx用Dockerファイル
│       └── nginx.conf  # nginx用設定ファイル
├── docker-compose.yml   # Docker-composeファイル
└── requirements.txt     # 使用モジュール記述ファイル
```
