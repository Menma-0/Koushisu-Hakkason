# ================================
# Stage 1: 開発環境
# ================================
FROM node:20-alpine AS dev
WORKDIR /app

# パッケージ定義だけ先にコピーしてインストール
# （ソースが変わってもキャッシュが効く）
COPY package.json package-lock.json* ./
RUN npm install

# ソースをコピー
COPY . .

# 開発サーバー起動
CMD ["npm", "run", "dev"]


# ================================
# Stage 2: ビルド
# ================================
FROM node:20-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build


# ================================
# Stage 3: 本番環境（軽量）
# ================================
FROM node:20-alpine AS prod
WORKDIR /app

# ビルド成果物だけコピー（node_modulesは不要）
COPY --from=builder /app/.output ./.output

ENV NODE_ENV=production
EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
