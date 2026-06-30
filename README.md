# AI-Admissions Platform · 教培机构 AI 招生顾问

> **多智能体 + RAG 知识库 + 自动化工作流，让招生主管 + 一线顾问的团队效能翻倍。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Node 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)

> 🎯 V1 聚焦 **K12 少儿编程教育**（8-15 岁），可平滑扩展至其他赛道

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
| 前端 | Next.js 14 · TypeScript · TailwindCSS · shadcn/ui |
| 后端 | FastAPI · SQLAlchemy 2.0 · Alembic |
| LLM | Claude 3.5 Sonnet · DeepSeek · OpenAI |
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
git clone https://github.com/yourname/ai-admissions-platform.git
cd ai-admissions-platform

# 2. 复制环境变量
cp .env.example .env
# 编辑 .env，填入 ANTHROPIC_API_KEY 或 DEEPSEEK_API_KEY

# 3. 启动基础服务（Postgres + Redis + Chroma）
docker compose up -d

# 4. 启动后端（FastAPI）
cd apps/api
uv sync
uv run uvicorn app.main:app --reload --port 8000

# 5. 启动前端（Next.js）
cd ../web
pnpm install
pnpm dev

# 6. 访问
# 前端 Demo：http://localhost:3000
# 后端 API：http://localhost:8000/docs
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
│   └── web/                      # Next.js 前端
│       ├── app/                  # App Router 页面
│       │   ├── demo/             # 演示台（对外）
│       │   └── page.tsx          # 首页
│       ├── components/
│       ├── lib/
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
- [ ] 数据模型 + Alembic 迁移
- [ ] LLM 适配层（Claude + DeepSeek）
- [ ] 招生顾问 Agent + 课程库 / FAQ 库
- [ ] Web 演示台（演示对话）
- [ ] 本地跑通 + 录 Demo 视频

### 📋 Phase 2 · 完整产品（第 3-4 周）

- [ ] 课程顾问 / 教务老师 / 内部助手 Agent
- [ ] 招生全链路工作流引擎
- [ ] 数据看板（漏斗 / 效能 / 知识库）
- [ ] 飞书 / 企微 Webhook

### 🚀 Phase 3 · 部署上线（第 5 周）

- [ ] Docker 化 + Vercel + Railway 部署
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

- [Anthropic Claude](https://www.anthropic.com/) — 主力 LLM
- [DeepSeek](https://www.deepseek.com/) — 备选 LLM
- [Chroma](https://www.trychroma.com/) — 向量数据库
- [FastAPI](https://fastapi.tiangolo.com/) — 后端框架
- [Next.js](https://nextjs.org/) — 前端框架
- [Dify](https://dify.ai/) / [Coze](https://www.coze.com/) — 设计灵感与生态参考