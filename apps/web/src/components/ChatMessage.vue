<script setup lang="ts">
import { computed } from 'vue';
import type { Message } from '@/types/chat';

const props = defineProps<{
  message: Message;
}>();

const time = computed(() => {
  const d = new Date(props.message.createdAt);
  return d.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
});

const isUser = computed(() => props.message.role === 'user');
</script>

<template>
  <article class="animate-slide-up font-mono">
    <!-- 时间戳 -->
    <div class="mb-1.5 flex items-center gap-2 text-xs text-ink-600">
      <span class="prompt">{{ isUser ? '›' : '›' }}</span>
      <span>[{{ time }}]</span>
      <span :class="isUser ? 'text-signal' : 'text-spark'">
        {{ isUser ? '用户' : '助手' }}
      </span>
      <span v-if="message.latencyMs" class="text-ink-600">
        · {{ message.latencyMs }}ms
      </span>
    </div>

    <!-- 消息内容 -->
    <div
      :class="[
        'prose-chat whitespace-pre-wrap rounded-lg border p-4 text-sm leading-relaxed',
        isUser
          ? 'border-signal/40 bg-signal/5 text-ink-900'
          : 'border-ink-300 bg-ink-100 text-ink-900',
      ]"
    >
      {{ message.content }}
    </div>

    <!-- 引用来源（RAG） -->
    <div
      v-if="message.citations && message.citations.length > 0"
      class="mt-2 space-y-1 border-l-2 border-grow/40 pl-3"
    >
      <div class="font-mono text-xs text-ink-600">📚 引用来源：</div>
      <div
        v-for="(cite, i) in message.citations"
        :key="i"
        class="flex items-center gap-2 font-mono text-xs text-ink-700"
      >
        <span class="text-grow">▸</span>
        <span class="text-ink-900">{{ cite.title }}</span>
        <span class="text-ink-600">({{ cite.score.toFixed(2) }})</span>
      </div>
    </div>
  </article>
</template>