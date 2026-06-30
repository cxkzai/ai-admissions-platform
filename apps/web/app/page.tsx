import Link from 'next/link';

const AGENTS = [
  {
    slug: 'admission-consultant',
    name: '招生顾问 Agent',
    desc: '7×24h 接待家长咨询，挖掘需求并推荐课程',
    icon: '🎯',
    color: 'from-blue-500 to-blue-700',
  },
  {
    slug: 'course-consultant',
    name: '课程顾问 Agent',
    desc: '深度课程对比、师资介绍、话术生成',
    icon: '📚',
    color: 'from-orange-500 to-orange-700',
  },
  {
    slug: 'academic-teacher',
    name: '教务老师 Agent',
    desc: '试听反馈分析与跟进话术',
    icon: '👨‍🏫',
    color: 'from-emerald-500 to-emerald-700',
  },
  {
    slug: 'internal-assistant',
    name: '内部知识助手',
    desc: 'SOP 检索、制度问答、跨库检索',
    icon: '💼',
    color: 'from-purple-500 to-purple-700',
  },
];

export default function HomePage() {
  return (
    <main className="container-page py-12">
      {/* Hero */}
      <section className="mb-16 text-center">
        <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-brand-50 px-4 py-1.5 text-sm font-medium text-brand-700">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-brand-400 opacity-75"></span>
            <span className="relative inline-flex h-2 w-2 rounded-full bg-brand-600"></span>
          </span>
          v0.1 · 多智能体 + RAG + 工作流
        </div>
        <h1 className="mb-4 text-5xl font-bold tracking-tight text-gray-900">
          AI-Admissions Platform
        </h1>
        <p className="mx-auto max-w-2xl text-lg text-gray-600">
          面向中小教培机构的 AI 招生顾问平台，覆盖
          <span className="font-medium text-gray-900">线索获取 → 需求挖掘 → 试听转化 → 老带新裂变</span>
          招生全链路。
        </p>
        <div className="mt-8 flex items-center justify-center gap-4">
          <Link href="/demo/chat" className="btn-primary">
            🚀 立即体验 Demo
          </Link>
          <Link
            href="https://github.com/yourname/ai-admissions-platform"
            className="btn-secondary"
            target="_blank"
          >
            ⭐ GitHub 仓库
          </Link>
        </div>
      </section>

      {/* Agent Matrix */}
      <section className="mb-16">
        <h2 className="mb-2 text-2xl font-bold text-gray-900">🤖 智能体矩阵</h2>
        <p className="mb-6 text-gray-600">4 类角色 Agent，覆盖招生全场景</p>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
          {AGENTS.map((agent) => (
            <Link
              key={agent.slug}
              href={`/demo/chat?agent=${agent.slug}`}
              className="card group cursor-pointer p-6 transition hover:shadow-md"
            >
              <div
                className={`mb-3 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${agent.color} text-2xl`}
              >
                {agent.icon}
              </div>
              <h3 className="mb-1 font-semibold text-gray-900 group-hover:text-brand-600">
                {agent.name}
              </h3>
              <p className="text-sm text-gray-600">{agent.desc}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="mb-16 grid grid-cols-1 gap-6 md:grid-cols-3">
        <div className="card p-6">
          <div className="mb-3 text-3xl">📖</div>
          <h3 className="mb-2 font-semibold">RAG 知识库</h3>
          <p className="text-sm text-gray-600">
            课程 / 师资 / 案例 / FAQ / 话术 / SOP 六类文档，向量化检索 + 重排序
          </p>
        </div>
        <div className="card p-6">
          <div className="mb-3 text-3xl">⚙️</div>
          <h3 className="mb-2 font-semibold">工作流引擎</h3>
          <p className="text-sm text-gray-600">
            招生全链路工作流，对接飞书 / 企微 Webhook，线索到成交自动跟进
          </p>
        </div>
        <div className="card p-6">
          <div className="mb-3 text-3xl">📊</div>
          <h3 className="mb-2 font-semibold">数据看板</h3>
          <p className="text-sm text-gray-600">
            招生漏斗、智能体效能、知识库命中率，话术 A/B 测试效果
          </p>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="card p-6">
        <h2 className="mb-4 font-semibold text-gray-900">🛠 技术栈</h2>
        <div className="grid grid-cols-2 gap-4 text-sm md:grid-cols-4">
          <div>
            <div className="mb-1 text-gray-500">前端</div>
            <div className="font-medium">Next.js 14 · TypeScript · TailwindCSS · shadcn/ui</div>
          </div>
          <div>
            <div className="mb-1 text-gray-500">后端</div>
            <div className="font-medium">FastAPI · SQLAlchemy 2.0 · Alembic</div>
          </div>
          <div>
            <div className="mb-1 text-gray-500">LLM</div>
            <div className="font-medium">Claude 3.5 Sonnet · DeepSeek · OpenAI</div>
          </div>
          <div>
            <div className="mb-1 text-gray-500">向量库</div>
            <div className="font-medium">Chroma · pgvector</div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-16 border-t border-gray-200 pt-8 text-center text-sm text-gray-500">
        <p>
          🎯 为中小教培机构打造 · MIT License · 由{' '}
          <a href="https://github.com/yourname" className="text-brand-600 hover:underline">
            张艺达
          </a>{' '}
          用心开发
        </p>
      </footer>
    </main>
  );
}