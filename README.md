# Koushisu-Hakkason

Supabase をデータ基盤とし、将来的に YOLO による画像認識を組み込む構成。

## 構成

```
Koushisu-Hakkason/
├── frontend/         Nuxt 3 (Vue 3 + TypeScript)
├── backend/          Go (net/http)
├── python-service/   Python (FastAPI) - YOLO推論用
├── docker-compose.yml
└── .env
```

| サービス | コンテナ名 | ポート | 役割 |
|----------|-----------|--------|------|
| frontend | vis_frontend | 3000 | UI |
| backend | vis_backend | 8080 | API ゲートウェイ |
| python-service | vis_python | 5001 | YOLO推論 (準備中) |

## 前提条件

- Docker Desktop がインストールされていること
- `.env` ファイルがプロジェクトルートにあること


## 起動方法

```bash
# 全サービスをビルド & 起動
docker compose up --build

# バックグラウンドで起動（ターミナルを占有しない）
docker compose up --build -d
```

起動後、ブラウザで http://localhost:3000 を開く。

## 停止方法

```bash
# フォアグラウンドで起動した場合は Ctrl+C、またはそのまま
docker compose down
```

## デバッグ方法

### ログの確認

```bash
# 全サービスのログ
docker compose logs

# 特定サービスのログ
docker compose logs frontend
docker compose logs backend
docker compose logs python-service

# リアルタイムで追いかける
docker compose logs -f backend
```

### コンテナの状態確認

```bash
docker compose ps
```

### API の動作確認

```bash
# バックエンド ヘルスチェック
curl http://localhost:8080/health

# Python サービス ヘルスチェック
curl http://localhost:5001/health

# 推論エンドポイント (Go → Python へプロキシ)
curl -X POST http://localhost:8080/predict
```

### フロントエンドのデバッグ

1. ブラウザで http://localhost:3000 を開く
2. DevTools を開く（F12 または Cmd+Option+I）
3. **Network** タブで API リクエスト・レスポンスを確認
4. **Console** タブで JavaScript エラーを確認

フロントエンド・Python はファイル保存で自動反映（ホットリロード）される。
Go バックエンドはコード変更後に `docker compose up --build -d` の再実行が必要。

### ライブラリの追加方法

| サービス | 手順 |
|----------|------|
| frontend | `frontend/package.json` に追記 → `docker compose up --build` |
| backend | `backend/go.mod` に追記（`go get`）→ `docker compose up --build` |
| python-service | `python-service/requirements.txt` に追記 → `docker compose up --build` |

## API エンドポイント一覧

### backend (Go) - `:8080`

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/health` | ヘルスチェック |
| POST | `/predict` | Python サービスへプロキシ |

### python-service (FastAPI) - `:5001`

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/health` | ヘルスチェック |
| POST | `/predict` | YOLO推論 (スタブ) |
