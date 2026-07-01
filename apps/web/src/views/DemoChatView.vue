<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import ChatMessage from '@/components/ChatMessage.vue';
import { useChat } from '@/composables/useChat';
import type { Agent, AgentSlug } from '@/types/chat';

const AGENTS: Agent[] = [
  {
    id: 'admission-consultant',
    slug: 'admission-consultant',
    name: '招生顾问',
    description: '7×24h 自动接待家长咨询',
    icon: '🎯',
    color: 'spark',
    tools: ['search_courses', 'book_audition', 'send_to_feishu'],
  },
  {
    id: 'course-consultant',
    slug: 'course-consultant',
    name: '课程顾问',
    description: '深度课程对比 + 师资介绍',
    icon: '📚',
    color: 'grow',
    tools: ['compare_courses', 'generate_script'],
  },
  {
    id: 'academic-teacher',
    slug: 'academic-teacher',
    name: '教务老师',
    description: '试听跟进 + 流失预警',
    icon: '👨‍🏫',
    color: 'signal',
    tools: ['analyze_feedback', 'generate_followup'],
  },
  {
    id: 'internal-assistant',
    slug: 'internal-assistant',
    name: '内部助手',
    description: 'SOP + 制度问答',
    icon: '💼',
    color: 'ink',
    tools: ['search_sop', 'search_courses'],
  },
];

const route = useRoute();

const currentSlug = computed<AgentSlug>(() => {
  const q = route.query.agent as AgentSlug | undefined;
  return q && AGENTS.some((a) => a.slug === q) ? q : 'admission-consultant';
});

const currentAgent = computed(() => AGENTS.find((a) => a.slug === currentSlug.value)!);

const { messages, loading, send, clear } = useChat(currentSlug.value);

const SAMPLE_QUESTIONS: Record<AgentSlug, string[]> = {
  'admission-consultant': [
    '我家孩子 8 岁，想学编程，你们有什么课？',
    '学费多少？有试听课吗？',
    '和编程猫/核桃编程比有什么优势？',
  ],
  'course-consultant': [
    'Scratch 和 Python 怎么选？',
    '高中数学想打 NOIP，学多久能参赛？',
    '我们的师资和课程体系能介绍一下吗？',
  ],
  'academic-teacher': [
    '试听课结束 24h 内的跟进话术怎么写？',
    '家长反馈"孩子觉得太难了"怎么应对？',
    '流失风险高的线索有什么特征？',
  ],
  'internal-assistant': [
    '试听课前要准备什么？',
    '退费流程是怎么走的？',
    '新员工入职 7 天流程是什么？',
  ],
};

const input = ref('');
const messagesContainer = ref<HTMLElement | null>(null);

watch(messages, async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
}, { deep: true });

const handleSend = () => {
  const text = input.value.trim();
  if (!text) return;
  send(text);
  input.value = '';
};

const handleSample = (text: string) => {
  send(text);
};
</script>

<template>
  <main class="flex h-screen flex-col bg-ink-50">
    <!-- 顶部 -->
    <header class="border-b border-ink-300 bg-ink-100">
      <div class="container-page flex items-center gap-4 py-3">
        <router-link
          to="/"
          class="text-sm text-ink-700 transition hover:text-spark"
        >
          ← 返回首页
        </router-link>
        <span class="text-ink-700">/</span>
        <span class="text-sm font-medium text-ink-900">智能体对话</span>
        <span class="ml-auto text-xs text-ink-600">
          {{ messages.length === 0 ? '演示模式（未连接后端）' : '已连接后端' }}
        </span>
      </div>

      <!-- Agent 切换 Tab -->
      <div class="container-page flex gap-1 overflow-x-auto pb-2">
        <button
          v-for="agent in AGENTS"
          :key="agent.slug"
          @click="$router.replace({ query: { agent: agent.slug } })"
          :class="[
            'flex items-center gap-2 whitespace-nowrap rounded-t-lg border-b-2 px-4 py-2 font-mono text-sm transition',
            currentSlug === agent.slug
              ? 'border-spark text-spark'
              : 'border-transparent text-ink-700 hover:text-ink-900',
          ]"
        >
          <span>{{ agent.icon }}</span>
          <span>{{ agent.name }}</span>
        </button>
      </div>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <!-- 左侧 Agent 介绍 -->
      <aside class="hidden w-72 shrink-0 overflow-y-auto border-r border-ink-300 bg-ink-200/60 p-6 lg:block">
        <div class="mb-4 text-4xl">{{ currentAgent.icon }}</div>
        <h2 class="mb-2 font-display text-xl font-bold text-ink-900">
          {{ currentAgent.name }}
        </h2>
        <p class="mb-6 text-sm text-ink-700">{{ currentAgent.description }}</p>

        <div class="mb-6">
          <div class="mb-2 font-mono text-xs text-ink-600">
            <span class="prompt">#</span> tools
          </div>
          <div class="flex flex-wrap gap-1.5">
            <span
              v-for="tool in currentAgent.tools"
              :key="tool"
              class="rounded border border-ink-300 bg-ink-50 px-2 py-0.5 font-mono text-xs text-ink-700"
            >
              {{ tool }}
            </span>
          </div>
        </div>

        <div class="mb-6">
          <div class="mb-2 font-mono text-xs text-ink-600">
            <span class="prompt">#</span> 我们的优点
          </div>
          <ul class="space-y-1.5 text-sm text-ink-700">
            <li class="flex gap-2"><span class="text-spark">▸</span> 多轮对话挖掘需求</li>
            <li class="flex gap-2"><span class="text-spark">▸</span> RAG 检索课程/师资</li>
            <li class="flex gap-2"><span class="text-spark">▸</span> Function Calling</li>
            <li class="flex gap-2"><span class="text-spark">▸</span> 情绪识别 & 话术适配</li>
          </ul>
        </div>

        <button
          @click="clear"
          class="w-full rounded border border-ink-300 bg-ink-50 px-3 py-2 font-mono text-xs text-ink-700 transition hover:border-spark hover:text-spark"
        >
          清空对话
        </button>
      </aside>

      <!-- 右侧对话区 -->
      <section class="flex flex-1 flex-col">
        <div
          ref="messagesContainer"
          class="flex-1 space-y-6 overflow-y-auto p-6"
        >
          <!-- 空状态 -->
          <div v-if="messages.length === 0" class="flex h-full flex-col items-center justify-center text-center">
            <div class="mb-4 text-5xl">💬</div>
            <h3 class="mb-2 font-display text-xl font-bold text-ink-900">
              ./start-conversation --agent={{ currentAgent.slug }}
            </h3>
            <p class="mb-8 max-w-md text-sm text-ink-700">
              试着问一个关于 <span class="text-spark">少儿编程</span> 的问题，或点击下方示例：
            </p>
            <div class="flex w-full max-w-md flex-col gap-2">
              <button
                v-for="q in SAMPLE_QUESTIONS[currentSlug]"
                :key="q"
                @click="handleSample(q)"
                class="group rounded border border-ink-300 bg-ink-100 p-3 text-left text-sm text-ink-700 transition hover:border-spark hover:bg-ink-200"
              >
                 {{ q }}
              </button>
            </div>
          </div>

          <!-- 消息列表 -->
          <ChatMessage
            v-for="m in messages"
            :key="m.id"
            :message="m"
          />

          <!-- Loading -->
          <div v-if="loading" class="flex animate-fade-in items-center gap-2 font-mono text-sm text-ink-600">
            
            <span>思考中</span>
            <span class="animate-pulse-dot">.</span>
            <span class="animate-pulse-dot" style="animation-delay: 0.2s">.</span>
            <span class="animate-pulse-dot" style="animation-delay: 0.4s">.</span>
          </div>
        </div>

        <!-- 输入框 -->
        <div class="border-t border-ink-300 bg-ink-100 p-4">
          <div class="flex items-center gap-2">
            
            <input
              v-model="input"
              @keydown.enter="handleSend"
              type="text"
              :disabled="loading"
              placeholder="输入你的问题，按 Enter 发送..."
              class="flex-1 rounded border border-ink-300 bg-ink-50 px-4 py-2.5 font-mono text-sm text-ink-900 placeholder-ink-500 focus:border-spark focus:outline-none disabled:opacity-50"
            />
            <button
              @click="handleSend"
              :disabled="loading || !input.trim()"
              class="rounded border border-spark bg-spark px-5 py-2.5 font-mono text-sm text-white transition hover:bg-spark-dark hover:text-ink-900 disabled:opacity-50"
            >
              send →
            </button>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>