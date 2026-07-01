<script setup lang="ts">
import { ref, computed } from 'vue';
import { useChat } from '@/composables/useChat';

// 左侧：传统顾问（固定话术模板）
const TRADITIONAL_REPLIES = [
  '您好！欢迎咨询码力星编程。',
  '我们提供 Scratch、Python、NOIP 等课程。',
  '请留下您的联系方式，我们会安排顾问与您联系。',
];

// 右侧：AI 顾问（真实调用）
const aiChat = useChat('admission-consultant');

const humanStep = ref(0);
const humanTyping = ref(false);

const handleHuman = () => {
  if (humanStep.value >= TRADITIONAL_REPLIES.length) return;
  humanTyping.value = true;
  setTimeout(() => {
    humanTyping.value = false;
    humanStep.value++;
  }, 1200);
};

const aiInput = ref('');

const handleAiSend = () => {
  const text = aiInput.value.trim();
  if (!text) return;
  aiChat.send(text);
  aiInput.value = '';
};

const humanDisplay = computed(() => TRADITIONAL_REPLIES.slice(0, humanStep.value));
</script>

<template>
  <main class="min-h-screen bg-ink-50">
    <!-- Header -->
    <header class="border-b border-ink-300 bg-ink-100">
      <div class="container-page flex items-center gap-4 py-3 font-mono text-sm">
        <router-link to="/" class="text-ink-700 transition hover:text-spark">
          ← 返回首页
        </router-link>
        <span class="text-ink-700">/</span>
        <span class="font-medium text-ink-900">人机对比</span>
      </div>
    </header>

    <!-- 标题 -->
    <section class="container-page py-12">
      <div class="mb-2 font-mono text-sm text-ink-600">
        <span class="prompt">#</span> 演示 · 震撼对比
      </div>
      <h1 class="mb-3 font-display text-3xl font-bold text-ink-900 md:text-4xl">
        // 人机对比演示
      </h1>
      <p class="max-w-2xl text-ink-700">
        同一句话，左边传统顾问 vs 右边 AI 招生顾问，直观对比响应速度、内容质量。
      </p>
    </section>

    <!-- 对比区 -->
    <section class="container-page pb-20">
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- 左侧：传统顾问 -->
        <div class="overflow-hidden rounded-lg border border-ink-300 bg-ink-100">
          <div class="border-b border-ink-300 bg-ink-200 px-4 py-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2 font-mono text-sm">
                <span>👤</span>
                <span class="text-ink-900">传统顾问</span>
                <span class="text-ink-600">(固定话术模板)</span>
              </div>
              <span class="font-mono text-xs text-spark">响应慢</span>
            </div>
          </div>

          <div class="space-y-3 p-6 font-mono text-sm">
            <div
              v-for="(msg, i) in humanDisplay"
              :key="i"
              class="animate-fade-in rounded border border-ink-300 bg-ink-50 p-3 text-ink-700"
            >
              <div class="mb-1 text-xs text-ink-600">[{{ i + 1 }}/3]</div>
              {{ msg }}
            </div>
            <div v-if="humanTyping" class="flex items-center gap-2 text-ink-600">
              
              <span>输入中</span>
              <span class="animate-pulse-dot">.</span>
              <span class="animate-pulse-dot" style="animation-delay: 0.2s">.</span>
              <span class="animate-pulse-dot" style="animation-delay: 0.4s">.</span>
            </div>
            <div
              v-if="humanStep >= TRADITIONAL_REPLIES.length"
              class="rounded border border-ink-300 bg-ink-50 p-3 text-xs text-ink-600"
            >
              <span class="prompt">#</span> 对话结束。顾问未识别需求，未引导留资，未推荐课程。
            </div>
          </div>

          <div class="border-t border-ink-300 p-4">
            <button
              v-if="humanStep < TRADITIONAL_REPLIES.length"
              @click="handleHuman"
              :disabled="humanTyping"
              class="w-full rounded border border-ink-300 bg-ink-50 px-4 py-2 font-mono text-sm text-ink-700 transition hover:border-spark hover:text-spark disabled:opacity-50"
            >
               模拟家长提问
            </button>
            <button
              v-else
              @click="humanStep = 0; humanTyping = false"
              class="w-full rounded border border-ink-300 bg-ink-50 px-4 py-2 font-mono text-sm text-ink-700 transition hover:border-spark hover:text-spark"
            >
               重新开始
            </button>
          </div>
        </div>

        <!-- 右侧：AI 顾问 -->
        <div class="overflow-hidden rounded-lg border border-spark bg-ink-100 glow-spark">
          <div class="border-b border-spark/40 bg-spark/10 px-4 py-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2 font-mono text-sm">
                <span>🤖</span>
                <span class="text-spark">AI 招生顾问</span>
                <span class="text-ink-700">(Claude + RAG)</span>
              </div>
              <span class="font-mono text-xs text-grow">响应快</span>
            </div>
          </div>

          <div class="space-y-3 p-6 font-mono text-sm">
            <div
              v-for="m in aiChat.messages.value"
              :key="m.id"
              :class="[
                'animate-fade-in rounded p-3',
                m.role === 'user'
                  ? 'border border-signal/30 bg-signal/5 text-ink-900'
                  : 'border border-spark/30 bg-spark/5 text-ink-900',
              ]"
            >
              <div class="mb-1 text-xs text-ink-600">
                <span class="prompt">{{ m.role === 'user' ? '›' : '›' }}</span>
                {{ m.role }}
                <span v-if="m.latencyMs">· {{ m.latencyMs }}ms</span>
              </div>
              <div class="whitespace-pre-wrap">{{ m.content }}</div>
            </div>
            <div v-if="aiChat.loading.value" class="flex items-center gap-2 text-spark">
              
              <span>思考中</span>
              <span class="animate-pulse-dot">.</span>
              <span class="animate-pulse-dot" style="animation-delay: 0.2s">.</span>
              <span class="animate-pulse-dot" style="animation-delay: 0.4s">.</span>
            </div>
            <div
              v-if="aiChat.messages.value.length === 0"
              class="rounded border border-ink-300 bg-ink-50 p-4 text-center text-ink-600"
            >
              <div class="mb-2 text-3xl">💬</div>
              <div>试试发送一个问题，看 AI 如何回应</div>
            </div>
          </div>

          <div class="border-t border-ink-300 p-4">
            <div class="flex items-center gap-2">
              
              <input
                v-model="aiInput"
                @keydown.enter="handleAiSend"
                type="text"
                :disabled="aiChat.loading.value"
                placeholder="例如：我家孩子8岁想学编程..."
                class="flex-1 rounded border border-ink-300 bg-ink-50 px-3 py-2 font-mono text-sm text-ink-900 placeholder-ink-500 focus:border-spark focus:outline-none disabled:opacity-50"
              />
              <button
                @click="handleAiSend"
                :disabled="aiChat.loading.value || !aiInput.trim()"
                class="rounded border border-spark bg-spark px-4 py-2 font-mono text-sm text-white transition hover:bg-spark-dark hover:text-ink-900 disabled:opacity-50"
              >
                发送
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部对比总结 -->
      <div class="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3">
        <div class="rounded-lg border border-ink-300 bg-ink-100 p-5">
          <div class="mb-2 font-mono text-xs text-ink-600">
            <span class="prompt">#</span> 响应时间
          </div>
          <div class="font-display text-3xl font-bold text-ink-900">
            1.2s <span class="text-base text-ink-600">vs</span> 5min
          </div>
          <div class="mt-1 text-xs text-ink-700">AI 首响 vs 人工首响</div>
        </div>
        <div class="rounded-lg border border-ink-300 bg-ink-100 p-5">
          <div class="mb-2 font-mono text-xs text-ink-600">
            <span class="prompt">#</span> 引用次数
          </div>
          <div class="font-display text-3xl font-bold text-grow">
            2.4 <span class="text-base text-ink-600">vs</span> 0
          </div>
          <div class="mt-1 text-xs text-ink-700">平均引用知识库文档数</div>
        </div>
        <div class="rounded-lg border border-ink-300 bg-ink-100 p-5">
          <div class="mb-2 font-mono text-xs text-ink-600">
            <span class="prompt">#</span> 工具调用
          </div>
          <div class="font-display text-3xl font-bold text-spark">
            5 <span class="text-base text-ink-600">vs</span> 0
          </div>
          <div class="mt-1 text-xs text-ink-700">自动调用的工具数（搜课/预约/推送）</div>
        </div>
      </div>
    </section>
  </main>
</template>