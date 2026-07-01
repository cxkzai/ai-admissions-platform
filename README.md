# AI-Admissions Platform · 教培机构 AI 招生顾问

> **多智能体 + RAG 知识库 + 自动化工作流，让招生主管 + 一线顾问的团队效能翻倍。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Node 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)
[![Vue 3](https://img.shields.io/badge/Vue-3-4FC08D.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)

> 🎯 V1 聚焦 **K12 少儿编程教育**（8-15 岁），可平滑扩展至其他赛道

**🎨 设计语言**：家长友好 + IDE 细节 — Light mode 米白主背景、ink/spark/grow 配色、JetBrains Mono + Inter、`#` `>` 终端提示符——让非技术访客（家长、面试官）一打开就觉得亲切、清晰，同时保留 IDE 风的辨识度（macOS 三圆点、bg-grid、glow-spark）。

---

## ✨ 核心特性

- 🤖 **多角色智能体**：招生顾问 / 课程顾问 / 教务老师 / 内部助手 4 类 Agent
- 📖 **RAG 知识库**：课程 / 师资 / 案例 / FAQ / 话术 / SOP 六类文档，向量化检索 + 重排序
- ⚙️ **工作流引擎**：招生全链路编排（线索培育 → 试听转化 → 老带新裂变）
- 💬 **多通道对接**：飞书 / 企微 / 公众号 Webhook
- 📊 **数据看板**：招生漏斗 / 智能体效能 / 知识库命中率
- 🔌 **生态兼容**：工作流可导出为 Dify YAML，提示词模板兼容 Coze JSON

---

## 🛠 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 · Vite · TypeScript · TailwindCSS · 自研"深夜 IDE"设计 |
| 后端 | FastAPI · SQLAlchemy 2.0 · Alembic |
| LLM | **DeepSeek（主力）** · Claude 3.5 Sonnet · OpenAI（适配层一键切换） |
| 向量库 | Chroma（开发）/ pgvector（生产） |
| 数据库 | PostgreSQL 16 + pgvector |
| 缓存 | Redis 7 |
| 包管理 | uv（Python）+ pnpm（Node） |
| 部署 | Vercel（前端）+ Railway（后端）+ Docker Compose |

---

## 🚀 快速启动

### 前置要求

- Python 3.11+
- Node.js 20+
- pnpm 9+（`npm install -g pnpm`）
- uv（`pip install uv`）
- Docker Desktop（用于 Postgres + Redis + Chroma）

### 一键启动

```bash
# 1. 克隆仓库
git clone https://github.com/cxkzai/ai-admissions-platform.git
cd ai-admissions-platform

# 2. 复制环境变量
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY（必填）和 OPENAI_API_KEY（可选，Embedding 用）
# ⚠️ 不要把 .env 提交到 Git（已在 .gitignore）

# 3. 启动基础服务（Postgres + Redis + Chroma）
#    chroma 用 bash 内置 /dev/tcp 做健康检查（镜像精简无 curl）
docker compose up -d

# 4. 启动后端（FastAPI）
cd apps/api
uv sync                                        # 装 205 个包（含 torch / chromadb / unstructured）
uv run alembic upgrade head                    # 跑数据库迁移（PostgreSQL + pgvector）
uv run python -m scripts.ingest_kb             # 导入知识库到 Chroma（48 chunks）
uv run python -m app.main                      # 启动后端（reload 模式，端口 8000）

# 5. 启动前端（Vue 3）
cd ../web
pnpm install                                   # pnpm-workspace.yaml 已配 allowBuilds: esbuild / vue-demi
pnpm dev                                       # 启动 Vite dev server（端口 3000）

# 6. 访问
# 前端 Demo：http://localhost:3000
# 后端 API：http://localhost:8000/docs
# 健康检查：http://localhost:8000/api/v1/health
```

### 🌐 公网访问（可选，给面试官发链接）

```bash
# 用 ngrok 把 3000 端口暴露到公网（Vite proxy 内部转发到 8000，一条 tunnel 整条链路）
ngrok http 3000
# 输出 Forwarding 行：https://xxxx.ngrok-free.dev -> http://localhost:3000
# 把 https://xxxx.ngrok-free.dev 发给面试官即可（首次访问要点 "Visit Site" 跳过 ngrok 警告页）
```

---

## 📁 项目结构

```
ai-admissions-platform/
├── apps/
│   ├── api/                      # FastAPI 后端
│   │   ├── app/
│   │   │   ├── api/v1/           # 路由
│   │   │   ├── core/             # 配置、日志、安全
│   │   │   ├── services/         # 业务服务（agent / rag / workflow）
│   │   │   ├── models/           # SQLAlchemy 模型
│   │   │   ├── schemas/          # Pydantic schemas
│   │   │   ├── db/               # 数据库连接
│   │   │   ├── llm/              # LLM 适配层
│   │   │   └── main.py           # FastAPI 入口
│   │   ├── alembic/              # 数据库迁移
│   │   ├── tests/                # 单元测试
│   │   └── pyproject.toml
│   └── web/                      # Vue 3 + Vite 前端
│       ├── src/
│       │   ├── views/            # 页面（Home / DemoChat / DemoCompare / 404）
│       │   ├── components/       # 组件（TerminalHero / AgentCard / ChatMessage）
│       │   ├── composables/      # useChat 等组合式函数
│       │   ├── router/           # Vue Router 4
│       │   ├── lib/              # API 客户端
│       │   ├── types/            # 类型定义
│       │   ├── assets/styles/    # main.css with design tokens
│       │   ├── App.vue
│       │   └── main.ts
│       ├── index.html
│       ├── vite.config.ts
│       ├── tailwind.config.js
│       └── package.json
├── packages/
│   └── shared/                   # 前后端共享类型
├── data/
│   └── knowledge_base/           # 知识库原始文档
├── docker/
│   ├── docker-compose.yml
│   └── init-pgvector.sql
├── docs/
│   ├── PRD.md                    # 产品需求文档
│   ├── architecture.md           # 架构详细设计
│   └── api.md                    # API 文档
├── scripts/
│   ├── seed_data.py              # 种子数据
│   ├── ingest_kb.py              # 知识库导入
│   └── eval_rag.py               # RAG 评测
├── .github/
│   └── workflows/                # CI
├── README.md
├── LICENSE
└── pyproject.toml                # uv workspace 根
```

---

## 🗺 路线图

### ✅ Phase 1 · MVP（第 1-2 周）

- [x] 项目脚手架 + Docker + CI
- [x] 数据模型 + Alembic 迁移（PostgreSQL + pgvector）
- [x] LLM 适配层（DeepSeek 主力 + Claude / OpenAI 备选）
- [x] 招生顾问 Agent + 6 类知识库（RAG 跑通，48 chunks 索引）
- [x] Web 演示台（Vue 3 + Vite，真实后端对话联调）
- [x] 对话历史（sessionStorage 持久化，切 agent 自动清空 + 加载回放 + 合并更新）
- [x] 真实后端健康检查 + 错误提示 banner + 重试按钮
- [x] 本地跑通 + ngrok 公网暴露
- [x] 4 个 root cause bug 修复（workspace / chroma health / CORS / GBK emoji）

> **Phase 1 全部完成**。4 个 Agent 实际都已接好（超出 Phase 1 范围），见 Phase 2 部分。

### 📋 Phase 2 · 完整产品（第 3-4 周）

- [x] 课程顾问 / 教务老师 / 内部助手 Agent（**提前在 Phase 1 完成**）
- [ ] 招生全链路工作流引擎
- [ ] 数据看板（漏斗 / 效能 / 知识库）
- [ ] 飞书 / 企微 Webhook

### 🚀 Phase 3 · 部署上线（第 5 周）

- [x] Docker Compose 一键启动（Postgres + Redis + Chroma）
- [x] ngrok 公网暴露（演示用，临时域名）
- [ ] Vercel + Railway 正式部署
- [ ] 域名 + HTTPS + 监控
- [ ] README 完善 + 架构图 + Demo 视频

### ✨ Phase 4 · 打磨投递（第 6 周）

- [ ] GitHub 仓库优化（Topics / About / Pin）
- [ ] 录 5 分钟讲解视频
- [ ] 简历项目描述改写

详见 [PRD.md](./PRD.md) 第 9 章。

---

## 🤖 智能体矩阵

| Agent | 角色定位 | 核心能力 | 触发方式 |
|---|---|---|---|
| 🎯 招生顾问 | 对外主接待 | 需求挖掘、课程推荐、试听预约 | 家长咨询入口 |
| 📚 课程顾问 | 专业咨询 | 课程对比、师资介绍、话术生成 | 一线顾问手动 |
| 👨‍🏫 教务老师 | 试听跟进 | 反馈分析、跟进话术、流失预警 | 试听结束 + 定时 |
| 💼 内部助手 | 员工百事通 | SOP 检索、制度问答 | 员工主动查询 |

---

## 📖 文档

- [PRD.md](./PRD.md) — 产品需求文档 v0.2
- [docs/architecture.md](./docs/architecture.md) — 架构详细设计（待补充）
- [docs/api.md](./docs/api.md) — API 文档（FastAPI 自动生成 `/docs`）

---

## 🆚 与开源智能体平台的差异化

| 能力 | AI-Admissions | Dify | Coze | 扣子 | FastGPT |
|---|---|---|---|---|---|
| 自研代码 | ✅ 100% | ❌ | ❌ | ❌ | ❌ |
| 多 Agent 协作 | ✅ 4 类角色 | ⚠️ | ⚠️ | ⚠️ | ❌ |
| RAG 自定义切片 | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ |
| Function Calling | ✅ 完全自定义 | ✅ | ✅ | ✅ | ⚠️ |
| 工作流可视化编辑 | V2（预留） | ✅ | ✅ | ✅ | ⚠️ |
| 工作流导出兼容 | ✅ | - | - | - | - |
| 垂直行业场景化 | ✅ 教培招生 | ❌ 通用 | ❌ 通用 | ❌ 通用 | ❌ 通用 |

详见 [PRD §3.8](./PRD.md)。

---

## 📝 License

MIT © 2026 张艺达

---

## 🙏 致谢

- [DeepSeek](https://www.deepseek.com/) — 主力 LLM（中文好、¥1/M token 便宜、面试官有代入感）
- [Anthropic Claude](https://www.anthropic.com/) — 备选 LLM（演示效果最佳）
- [Chroma](https://www.trychroma.com/) — 向量数据库
- [FastAPI](https://fastapi.tiangolo.com/) — 后端框架
- [Vue 3](https://vuejs.org/) — 前端框架
- [Dify](https://dify.ai/) / [Coze](https://www.coze.com/) — 设计灵感与生态参考
- [ngrok](https://ngrok.com/) — 公网隧道（演示给面试官用）