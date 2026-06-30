<script setup lang="ts">
import type { Agent } from '@/types/chat';

defineProps<{
  agent: Agent;
  index: number;
}>();
</script>

<template>
  <router-link
    :to="{ path: '/demo/chat', query: { agent: agent.slug } }"
    class="group relative block overflow-hidden rounded-lg border border-ink-800 bg-ink-900 p-6 transition hover:border-spark hover:shadow-lg hover:shadow-spark/10"
  >
    <!-- 顶部编号条 -->
    <div class="absolute left-0 top-0 h-full w-1 bg-ink-800 transition group-hover:bg-spark"></div>

    <!-- 编号 + 图标 -->
    <div class="mb-4 flex items-start justify-between">
      <span class="font-mono text-xs text-ink-500">
        [{{ String(index + 1).padStart(2, '0') }}]
      </span>
      <span class="text-3xl">{{ agent.icon }}</span>
    </div>

    <!-- 名称 -->
    <h3 class="mb-2 font-display text-lg font-bold text-ink-100 group-hover:text-spark">
      {{ agent.name }}
    </h3>

    <!-- 描述 -->
    <p class="mb-4 text-sm leading-relaxed text-ink-300">
      {{ agent.description }}
    </p>

    <!-- 工具列表 -->
    <div class="mb-4 flex flex-wrap gap-1.5">
      <span
        v-for="tool in agent.tools"
        :key="tool"
        class="rounded border border-ink-700 bg-ink-950 px-2 py-0.5 font-mono text-xs text-ink-300"
      >
        {{ tool }}
      </span>
    </div>

    <!-- 底部状态 -->
    <div class="flex items-center gap-2 border-t border-ink-800 pt-3 font-mono text-xs">
      <span class="relative flex h-2 w-2">
        <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-grow opacity-75"></span>
        <span class="relative inline-flex h-2 w-2 rounded-full bg-grow"></span>
      </span>
      <span class="text-ink-500">online</span>
      <span class="ml-auto text-ink-500 transition group-hover:text-spark">try →</span>
    </div>
  </router-link>
</template>