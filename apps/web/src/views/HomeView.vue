<script setup lang="ts">
import TerminalHero from '@/components/TerminalHero.vue';
import AgentCard from '@/components/AgentCard.vue';
import type { Agent } from '@/types/chat';

const AGENTS: Agent[] = [
  {
    id: '1',
    slug: 'admission-consultant',
    name: '招生顾问 Agent',
    description: '7×24h 自动接待家长咨询，挖掘需求并推荐课程，是机构对外的首席咨询师。',
    icon: '🎯',
    color: 'spark',
    tools: ['search_courses', 'search_teachers', 'check_schedule', 'book_audition', 'send_to_feishu'],
  },
  {
    id: '2',
    slug: 'course-consultant',
    name: '课程顾问 Agent',
    description: '辅助一线顾问做课程对比、师资介绍、竞品话术、报价单生成等专业咨询。',
    icon: '📚',
    color: 'grow',
    tools: ['compare_courses', 'generate_script', 'export_quote_pdf'],
  },
  {
    id: '3',
    slug: 'academic-teacher',
    name: '教务老师 Agent',
    description: '负责试听课后跟进，分析反馈、生成跟进话术、识别流失风险。',
    icon: '👨‍🏫',
    color: 'signal',
    tools: ['analyze_feedback', 'generate_followup', 'risk_score'],
  },
  {
    id: '4',
    slug: 'internal-assistant',
    name: '内部知识助手',
    description: '员工的"百事通"，沉淀 SOP 与制度问答，支持跨库检索。',
    icon: '💼',
    color: 'ink',
    tools: ['search_sop', 'search_courses', 'search_cases'],
  },
];

const STACK = [
  { layer: 'frontend', items: ['Vue 3', 'Vite', 'TypeScript', 'TailwindCSS'] },
  { layer: 'backend', items: ['FastAPI', 'SQLAlchemy 2.0', 'Alembic', 'PostgreSQL 16'] },
  { layer: 'llm', items: ['Claude 3.5 Sonnet', 'DeepSeek', 'OpenAI', 'Function Calling'] },
  { layer: 'rag', items: ['Chroma', 'pgvector', 'bge-m3', 'Rerank'] },
];
</script>

<template>
  <main>
    <TerminalHero />

    <!-- 智能体矩阵 -->
    <section class="border-t border-ink-300 bg-ink-200/60 py-20">
      <div class="container-page">
        <header class="mb-12">
          <h2 class="font-display text-3xl font-bold text-ink-900 md:text-4xl">
            // 智能体矩阵
          </h2>
          <p class="mt-3 max-w-2xl text-ink-700">
            4 类角色 Agent 覆盖招生全场景。每个 Agent 都有专属 Prompt、工具集与知识库绑定。
          </p>
        </header>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
          <AgentCard
            v-for="(agent, i) in AGENTS"
            :key="agent.id"
            :agent="agent"
            :index="i"
          />
        </div>
      </div>
    </section>

    <!-- 技术栈 -->
    <section class="border-t border-ink-300 py-20">
      <div class="container-page">
        <header class="mb-12">
          <h2 class="font-display text-3xl font-bold text-ink-900 md:text-4xl">
            // 技术栈
          </h2>
          <p class="mt-3 max-w-2xl text-ink-700">
            全栈自研，覆盖从 LLM 适配到向量检索的完整链路。
          </p>
        </header>

        <div class="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-4">
          <div
            v-for="stack in STACK"
            :key="stack.layer"
            class="rounded-lg border border-ink-300 bg-ink-100 p-5"
          >
            <div class="mb-3 flex items-center gap-2">
              
              <span class="font-mono text-sm text-ink-600">{{ stack.layer }}</span>
            </div>
            <ul class="space-y-1.5">
              <li
                v-for="item in stack.items"
                :key="item"
                class="flex items-center gap-2 text-sm text-ink-900"
              >
                <span class="text-spark">▸</span>
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- 差异化对比 -->
    <section class="border-t border-ink-300 bg-ink-200/60 py-20">
      <div class="container-page">
        <header class="mb-12">
          <h2 class="font-display text-3xl font-bold text-ink-900 md:text-4xl">
            // 与 Dify / Coze 的对比优势
          </h2>
        </header>

        <div class="overflow-x-auto rounded-lg border border-ink-300">
          <table class="w-full min-w-[640px] font-mono text-sm">
            <thead class="bg-ink-200 text-xs font-bold text-ink-700">
              <tr>
                <th class="px-4 py-3 text-left">能力</th>
                <th class="px-4 py-3 text-center text-spark">本项目</th>
                <th class="px-4 py-3 text-center">Dify</th>
                <th class="px-4 py-3 text-center">Coze</th>
                <th class="px-4 py-3 text-center">FastGPT</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-ink-300 bg-ink-100 text-ink-700">
              <tr>
                <td class="px-4 py-3 font-semibold text-ink-900">自研代码</td>
                <td class="px-4 py-3 text-center font-bold text-spark">✓ 100%</td>
                <td class="px-4 py-3 text-center">—</td>
                <td class="px-4 py-3 text-center">—</td>
                <td class="px-4 py-3 text-center">—</td>
              </tr>
              <tr>
                <td class="px-4 py-3 font-semibold text-ink-900">多角色 Agent</td>
                <td class="px-4 py-3 text-center font-bold text-spark">✓ 4 类</td>
                <td class="px-4 py-3 text-center">需编排</td>
                <td class="px-4 py-3 text-center">需编排</td>
                <td class="px-4 py-3 text-center">✗</td>
              </tr>
              <tr>
                <td class="px-4 py-3 font-semibold text-ink-900">RAG 自定义切片</td>
                <td class="px-4 py-3 text-center font-bold text-spark">✓</td>
                <td class="px-4 py-3 text-center">部分</td>
                <td class="px-4 py-3 text-center">部分</td>
                <td class="px-4 py-3 text-center">✓</td>
              </tr>
              <tr>
                <td class="px-4 py-3 font-semibold text-ink-900">Function Calling</td>
                <td class="px-4 py-3 text-center font-bold text-spark">✓ 完全自定义</td>
                <td class="px-4 py-3 text-center">✓</td>
                <td class="px-4 py-3 text-center">✓</td>
                <td class="px-4 py-3 text-center">弱</td>
              </tr>
              <tr>
                <td class="px-4 py-3 font-semibold text-ink-900">工作流导出兼容</td>
                <td class="px-4 py-3 text-center font-bold text-spark">✓</td>
                <td class="px-4 py-3 text-center">—</td>
                <td class="px-4 py-3 text-center">—</td>
                <td class="px-4 py-3 text-center">—</td>
              </tr>
              <tr>
                <td class="px-4 py-3 font-semibold text-ink-900">教培垂直场景</td>
                <td class="px-4 py-3 text-center font-bold text-spark">✓</td>
                <td class="px-4 py-3 text-center">通用</td>
                <td class="px-4 py-3 text-center">通用</td>
                <td class="px-4 py-3 text-center">通用</td>
              </tr>
              <tr>
                <td class="px-4 py-3 font-semibold text-ink-900">成本（LLM 调用）</td>
                <td class="px-4 py-3 text-center font-bold text-spark">¥1/M</td>
                <td class="px-4 py-3 text-center">$3/M</td>
                <td class="px-4 py-3 text-center">$3/M</td>
                <td class="px-4 py-3 text-center">自托管</td>
              </tr>
              <tr>
                <td class="px-4 py-3 font-semibold text-ink-900">私有化部署</td>
                <td class="px-4 py-3 text-center font-bold text-spark">✓</td>
                <td class="px-4 py-3 text-center">✓</td>
                <td class="px-4 py-3 text-center">—</td>
                <td class="px-4 py-3 text-center">✓</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-ink-300 bg-ink-200/60 py-12">
      <div class="container-page">
        <div class="grid grid-cols-1 gap-8 md:grid-cols-3">

          <!-- 品牌 -->
          <div>
            <div class="mb-3 flex items-center gap-2">
              <span class="prompt font-mono">$</span>
              <span class="font-display text-lg font-bold text-ink-900">AI 招生顾问</span>
            </div>
            <p class="mb-4 text-sm leading-relaxed text-ink-700">
              面向中小教培机构的 AI 招生顾问平台。多智能体 + RAG + 工作流，端到端自研。
            </p>
            <p class="font-mono text-xs text-ink-600">
              <span class="prompt">//</span> 开源协议 · 2026
            </p>
          </div>

          <!-- 链接 -->
          <div>
            <h4 class="mb-4 font-mono text-xs uppercase tracking-wider text-ink-600">
              <span class="prompt">#</span> 相关链接
            </h4>
            <ul class="space-y-2 text-sm">
              <li>
                <a
                  href="https://github.com/cxkzai/ai-admissions-platform"
                  target="_blank"
                  rel="noopener"
                  class="inline-flex items-center gap-2 text-ink-700 transition hover:text-spark"
                >
                  <span class="prompt">git</span> 源码仓库 →
                </a>
              </li>
              <li>
                <a
                  href="/demo/chat"
                  class="inline-flex items-center gap-2 text-ink-700 transition hover:text-spark"
                >
                   智能体体验 →
                </a>
              </li>
              <li>
                <a
                  href="/demo/compare"
                  class="inline-flex items-center gap-2 text-ink-700 transition hover:text-spark"
                >
                   人机对比 →
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/cxkzai/ai-admissions-platform/blob/main/PRD.md"
                  target="_blank"
                  rel="noopener"
                  class="inline-flex items-center gap-2 text-ink-700 transition hover:text-spark"
                >
                   产品文档 →
                </a>
              </li>
            </ul>
          </div>

          <!-- 数据指标 -->
          <div>
            <h4 class="mb-4 font-mono text-xs uppercase tracking-wider text-ink-600">
              <span class="prompt">#</span> 项目数据
            </h4>
            <dl class="space-y-1.5 font-mono text-sm">
              <div class="flex items-baseline justify-between">
                <dt class="font-semibold text-ink-800">智能体</dt>
                <dd class="font-bold text-ink-900">
                  <span class="text-spark">4</span> 类
                </dd>
              </div>
              <div class="flex items-baseline justify-between">
                <dt class="font-semibold text-ink-800">知识库</dt>
                <dd class="font-bold text-ink-900">
                  <span class="text-spark">6</span> 类 / <span class="text-grow">32</span> 评测
                </dd>
              </div>
              <div class="flex items-baseline justify-between">
                <dt class="font-semibold text-ink-800">代码量</dt>
                <dd class="font-bold text-ink-900">
                  <span class="text-spark">~7k</span> 行
                </dd>
              </div>
              <div class="flex items-baseline justify-between">
                <dt class="font-semibold text-ink-800">LLM 引擎</dt>
                <dd class="font-bold text-ink-900">
                  <span class="text-spark">3</span> 个可切换
                </dd>
              </div>
            </dl>
          </div>

        </div>

        <!-- 底部署名 -->
        <div class="mt-10 border-t border-ink-300 pt-6 font-mono text-xs text-ink-600">
          <div class="flex flex-col items-start justify-between gap-2 sm:flex-row sm:items-center">
            <span>
              <span class="prompt">//</span> 由 张艺达 制作
            </span>
            <span class="text-ink-400">·</span>
            <span>
               查看 README 了解更多
            </span>
          </div>
        </div>
      </div>
    </footer>
  </main>
</template>