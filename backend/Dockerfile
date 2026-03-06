# ================================
# Stage 1: ビルド
# ================================
FROM golang:1.22-alpine AS builder
WORKDIR /app

# go.mod と go.sum を先にコピーしてダウンロード
# （ソースが変わってもキャッシュが効く）
COPY go.mod go.sum ./
RUN go mod download

# ソースをコピーしてビルド
COPY . .
RUN go build -o main .


# ================================
# Stage 2: 本番環境（超軽量）
# ================================
FROM alpine:latest AS prod

# セキュリティのため非rootユーザーで実行
RUN adduser -D appuser
USER appuser

WORKDIR /app

# バイナリだけコピー（Goのソースは不要）
COPY --from=builder /app/main .

EXPOSE 8080

CMD ["./main"]
