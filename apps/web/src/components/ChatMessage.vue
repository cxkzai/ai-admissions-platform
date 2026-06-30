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
    <div class="mb-1.5 flex items-center gap-2 text-xs text-ink-500">
      <span class="prompt">{{ isUser ? '$' : '>' }}</span>
      <span>[{{ time }}]</span>
      <span :class="isUser ? 'text-signal' : 'text-spark'">
        {{ isUser ? 'user' : 'assistant' }}
      </span>
      <span v-if="message.latencyMs" class="text-ink-500">
        · {{ message.latencyMs }}ms
      </span>
    </div>

    <!-- 消息内容 -->
    <div
      :class="[
        'prose-chat whitespace-pre-wrap rounded-lg border p-4 text-sm leading-relaxed',
        isUser
          ? 'border-signal/30 bg-signal/5 text-ink-100'
          : 'border-ink-700 bg-ink-900 text-ink-100',
      ]"
    >
      {{ message.content }}
    </div>

    <!-- 引用来源（RAG） -->
    <div
      v-if="message.citations && message.citations.length > 0"
      class="mt-2 space-y-1 border-l-2 border-grow/40 pl-3"
    >
      <div class="font-mono text-xs text-ink-500">📚 references:</div>
      <div
        v-for="(cite, i) in message.citations"
        :key="i"
        class="flex items-center gap-2 font-mono text-xs text-ink-300"
      >
        <span class="text-grow">▸</span>
        <span class="text-ink-100">{{ cite.title }}</span>
        <span class="text-ink-500">({{ cite.score.toFixed(2) }})</span>
      </div>
    </div>
  </article>
</template>