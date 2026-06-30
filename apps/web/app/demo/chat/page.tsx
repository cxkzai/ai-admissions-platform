'use client';

import { useState } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

const SAMPLE_QUESTIONS = [
  '我家孩子 8 岁，想学编程，你们有什么课？',
  'Scratch 和 Python 怎么选？',
  '学费多少？有试听课吗？',
];

export default function ChatDemoPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const send = async (text: string) => {
    if (!text.trim() || loading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      // TODO: 接入真实 API
      // const res = await fetch('/api/proxy/chat/message', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ message: text, agent_slug: 'admission-consultant' }),
      // });
      // const data = await res.json();

      // 演示用 Mock 回复
      await new Promise((r) => setTimeout(r, 1000));
      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content:
          '🎯 [演示模式] 这是 AI-Admissions Platform 的招生顾问 Agent 占位回复。\n\n' +
          '完整功能将在 Phase 1 实现：\n' +
          '• 多轮对话挖掘需求\n' +
          '• RAG 检索课程库（6 门编程课）\n' +
          '• Function Calling 预约试听\n' +
          '• 飞书群消息推送\n\n' +
          '请按 PRD 9.2 Phase 1 计划推进实现。',
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container-page py-8">
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[300px_1fr]">
        {/* 左侧：Agent 介绍 */}
        <aside className="card p-6">
          <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-blue-700 text-2xl">
            🎯
          </div>
          <h2 className="mb-2 font-semibold text-gray-900">招生顾问 Agent</h2>
          <p className="mb-4 text-sm text-gray-600">
            7×24h 自动接待家长咨询，挖掘需求并推荐课程
          </p>

          <div className="space-y-2 text-xs text-gray-500">
            <div>
              <div className="mb-1 font-medium text-gray-700">核心能力</div>
              <ul className="ml-4 list-disc space-y-1">
                <li>多轮需求挖掘</li>
                <li>课程智能推荐（RAG）</li>
                <li>试听预约（Function Calling）</li>
                <li>情绪识别与话术适配</li>
              </ul>
            </div>
            <div>
              <div className="mb-1 font-medium text-gray-700">工具调用</div>
              <ul className="ml-4 list-disc space-y-1">
                <li>search_courses</li>
                <li>search_teachers</li>
                <li>check_schedule</li>
                <li>book_audition</li>
                <li>send_to_feishu</li>
              </ul>
            </div>
          </div>
        </aside>

        {/* 右侧：对话窗口 */}
        <div className="card flex h-[600px] flex-col">
          {/* 消息列表 */}
          <div className="flex-1 space-y-4 overflow-y-auto p-6">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center text-center">
                <div className="mb-4 text-4xl">💬</div>
                <h3 className="mb-2 text-lg font-semibold text-gray-900">
                  开始和招生顾问对话
                </h3>
                <p className="mb-6 max-w-md text-sm text-gray-600">
                  试着问一个关于 K12 少儿编程的问题
                </p>
                <div className="flex flex-col gap-2">
                  {SAMPLE_QUESTIONS.map((q) => (
                    <button
                      key={q}
                      onClick={() => send(q)}
                      className="btn-secondary text-left text-sm"
                      disabled={loading}
                    >
                      💡 {q}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((m) => (
                <div
                  key={m.id}
                  className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-2.5 ${
                      m.role === 'user'
                        ? 'bg-brand-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <pre className="prose-chat whitespace-pre-wrap font-sans">
                      {m.content}
                    </pre>
                  </div>
                </div>
              ))
            )}
            {loading && (
              <div className="flex justify-start">
                <div className="rounded-lg bg-gray-100 px-4 py-2.5 text-gray-500">
                  <span className="animate-pulse">思考中...</span>
                </div>
              </div>
            )}
          </div>

          {/* 输入框 */}
          <div className="border-t border-gray-200 p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && send(input)}
                placeholder="输入问题..."
                className="flex-1 rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500"
                disabled={loading}
              />
              <button
                onClick={() => send(input)}
                disabled={loading || !input.trim()}
                className="btn-primary"
              >
                发送
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}