# ===== AI-Admissions Platform · Next.js Dockerfile =====

FROM node:20-alpine AS base
RUN corepack enable && corepack prepare [email protected] --activate

WORKDIR /app

# 依赖文件
COPY package.json pnpm-lock.yaml* ./
COPY tsconfig.json next.config.mjs tailwind.config.ts postcss.config.mjs ./
COPY app ./app
COPY components ./components
COPY lib ./lib
COPY public ./public

# 安装
RUN pnpm install --frozen-lockfile

# 构建
RUN pnpm build

EXPOSE 3000

CMD ["pnpm", "start"]