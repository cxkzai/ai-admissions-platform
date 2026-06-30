<script setup lang="ts">
import { ref, onMounted } from 'vue';

const props = withDefaults(
  defineProps<{
    title?: string;
    subtitle?: string;
    command?: string;
    outputLines?: string[];
  }>(),
  {
    title: 'AI-Admissions Platform',
    subtitle: '教培机构 AI 招生顾问平台 · 多智能体 + RAG + 工作流',
    command: './ai-admissions --start --mode=demo',
    outputLines: () => [
      '[ok] loading agent: admission-consultant',
      '[ok] loading agent: course-consultant',
      '[ok] loading agent: academic-teacher',
      '[ok] loading agent: internal-assistant',
      '[ok] indexing knowledge_base: 6 collections, 247 chunks',
      '[ok] ready. type a message to start.',
    ],
  },
);

const displayedLines = ref<string[]>([]);
const cursorVisible = ref(true);
const isLoaded = ref(false);

onMounted(async () => {
  // 逐行打印，模拟终端启动
  for (const line of props.outputLines) {
    await new Promise((r) => setTimeout(r, 220));
    displayedLines.value.push(line);
  }
  await new Promise((r) => setTimeout(r, 200));
  isLoaded.value = true;
});

// 终端光标闪烁
setInterval(() => {
  cursorVisible.value = !cursorVisible.value;
}, 530);
</script>

<template>
  <section class="relative overflow-hidden bg-grid bg-ink-950">
    <!-- 顶部窗口装饰条 -->
    <div class="border-b border-ink-800">
      <div class="container-page flex items-center gap-2 py-3 font-mono text-xs text-ink-500">
        <span class="h-2.5 w-2.5 rounded-full bg-spark"></span>
        <span class="h-2.5 w-2.5 rounded-full bg-grow"></span>
        <span class="h-2.5 w-2.5 rounded-full bg-signal"></span>
        <span class="ml-3 hidden sm:inline">~/ai-admissions-platform — bash</span>
      </div>
    </div>

    <div class="container-page py-20 md:py-28">
      <!-- 标题区 -->
      <div class="mb-10">
        <div class="mb-4 inline-flex items-center gap-2 rounded-sm border border-ink-700 bg-ink-900 px-3 py-1 font-mono text-xs">
          <span class="prompt">$</span>
          <span class="text-ink-300">{{ command }}</span>
        </div>

        <h1 class="mb-4 font-display text-mega font-bold tracking-tight">
          <span class="text-ink-100">{{ title }}</span>
          <span class="block text-spark">教培 AI 招生</span>
        </h1>

        <p class="max-w-2xl text-base leading-relaxed text-ink-300 md:text-lg">
          {{ subtitle }}
        </p>
      </div>

      <!-- 终端输出区 -->
      <div class="mb-10 overflow-hidden rounded-lg border border-ink-700 bg-ink-900">
        <div class="border-b border-ink-700 bg-ink-800 px-4 py-2 font-mono text-xs text-ink-500">
          stdout
        </div>
        <div
          class="space-y-1 p-5 font-mono text-sm leading-relaxed"
          role="log"
          aria-live="polite"
          aria-atomic="false"
          aria-label="项目启动序列"
        >
          <div v-for="(line, i) in displayedLines" :key="i" class="animate-fade-in text-grow">
            {{ line }}
          </div>
          <div v-if="!isLoaded" class="font-mono text-ink-300">
            <span class="prompt">$</span>
            <span :class="{ 'opacity-0': !cursorVisible }">▌</span>
          </div>
          <div v-else class="font-mono text-ink-100">
            <span class="prompt">$</span>
            <span :class="{ 'opacity-0': !cursorVisible }" class="text-spark">▌</span>
          </div>
        </div>
      </div>

      <!-- CTA 按钮 -->
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
        <router-link
          to="/demo/chat"
          class="group inline-flex items-center justify-center gap-2 rounded-lg border border-spark bg-spark px-6 py-3 font-mono text-sm font-medium text-ink-950 shadow-lg glow-spark transition hover:bg-spark-dark hover:text-ink-100"
        >
          <span class="prompt text-ink-950 group-hover:text-ink-100">$</span>
          ./start-demo
          <span class="text-ink-950/70 group-hover:text-ink-100/70">→</span>
        </router-link>

        <router-link
          to="/demo/compare"
          class="inline-flex items-center justify-center gap-2 rounded-lg border border-ink-700 bg-ink-900 px-6 py-3 font-mono text-sm text-ink-100 transition hover:border-grow hover:text-grow"
        >
          <span class="prompt">#</span>
          ./compare-human-vs-ai
        </router-link>

        <a
          href="https://github.com/cxkzai/ai-admissions-platform"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center justify-center gap-2 rounded-lg px-6 py-3 font-mono text-sm text-ink-300 transition hover:text-ink-100"
        >
          <span class="prompt">git</span>
          clone repo →
        </a>
      </div>
    </div>
  </section>
</template>