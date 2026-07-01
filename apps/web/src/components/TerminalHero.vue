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
    title: 'AI 招生顾问平台',
    subtitle: '面向中小教培机构的 AI 招生顾问 · 7×24h 自动接待家长咨询，提升招生团队效能',
    command: './启动演示 --模式=demo',
    outputLines: () => [
      '[ok] loading agent: admission-consultant',
      '[完成] 加载招生顾问 Agent',
      '[ok] loading agent: course-consultant',
      '[完成] 加载课程顾问 Agent',
      '[ok] loading agent: academic-teacher',
      '[完成] 加载教务老师 Agent',
      '[ok] loading agent: internal-assistant',
      '[完成] 加载内部知识助手',
      '[ok] indexing knowledge_base: 6 collections, 247 chunks',
      '[完成] 索引知识库：6 个分类，共 247 条资料',
      '[ready] type a message to start.',
      '[就绪] 系统已就绪。请输入您的问题开始体验。',
    ],
  },
);

const displayedLines = ref<string[]>([]);
const cursorVisible = ref(true);
const isLoaded = ref(false);

onMounted(async () => {
  // 逐行打印，模拟终端启动
  for (const line of props.outputLines) {
    await new Promise((r) => setTimeout(r, 420));
    displayedLines.value.push(line);
  }
  await new Promise((r) => setTimeout(r, 400));
  isLoaded.value = true;
});

// 终端光标闪烁
setInterval(() => {
  cursorVisible.value = !cursorVisible.value;
}, 530);
</script>

<template>
  <section class="relative overflow-hidden bg-grid bg-ink-50">
    <!-- 顶部窗口装饰条 -->
    <div class="border-b border-ink-300 bg-ink-100">
      <div class="container-page flex items-center gap-2 py-3 font-mono text-xs text-ink-600">
        <span class="h-2.5 w-2.5 rounded-full bg-spark"></span>
        <span class="h-2.5 w-2.5 rounded-full bg-grow"></span>
        <span class="h-2.5 w-2.5 rounded-full bg-signal"></span>
        <span class="ml-3 hidden sm:inline">AI 招生平台 · 已就绪</span>
      </div>
    </div>

    <div class="container-page py-20 md:py-28">
      <!-- 标题区 -->
      <div class="mb-10">
        <div class="mb-4 inline-flex items-center gap-2 rounded-sm border border-ink-400 bg-ink-100 px-3 py-1 font-mono text-xs">
          
          <span class="text-ink-700">{{ command }}</span>
        </div>

        <h1 class="mb-4 font-display text-mega font-bold tracking-tight">
          <span class="text-ink-900">{{ title }}</span>
          <span class="block text-spark">让招生更高效</span>
        </h1>

        <p class="max-w-2xl text-base leading-relaxed text-ink-700 md:text-lg">
          {{ subtitle }}
        </p>
      </div>

      <!-- 终端输出区 -->
      <div class="mb-10 overflow-hidden rounded-lg border border-ink-300 bg-ink-100 shadow-sm">
        <div class="border-b border-ink-300 bg-ink-200 px-4 py-2 font-mono text-xs text-ink-600">
          系统输出
        </div>
        <div
          class="space-y-1 p-5 font-mono text-sm leading-relaxed"
          role="log"
          aria-live="polite"
          aria-atomic="false"
          aria-label="项目启动序列"
        >
          <div
            v-for="(line, i) in displayedLines"
            :key="i"
            :class="[
              'animate-fade-in pl-3',
              line.startsWith('[') && /[a-z]/.test(line.split(']')[0] + ']')
                ? 'text-ink-400 text-base italic border-l-2 border-ink-200'
                : 'text-ink-900 font-medium',
            ]"
          >
            {{ line }}
          </div>
          <div v-if="!isLoaded" class="font-mono text-ink-700">
            
            <span :class="{ 'opacity-0': !cursorVisible }">▌</span>
          </div>
          <div v-else class="font-mono text-ink-900">
            
            <span :class="{ 'opacity-0': !cursorVisible }" class="text-spark">▌</span>
          </div>
        </div>
      </div>

      <!-- CTA 按钮 -->
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
        <router-link
          to="/demo/chat"
          class="group inline-flex items-center justify-center gap-2 rounded-lg bg-spark px-6 py-3 font-mono text-sm font-medium text-white shadow-md glow-spark transition hover:bg-spark-dark"
        >
          <span class="prompt text-white">$</span>
          立即体验 Demo
          <span class="text-white/70">→</span>
        </router-link>

        <router-link
          to="/demo/compare"
          class="inline-flex items-center justify-center gap-2 rounded-lg border border-ink-400 bg-ink-100 px-6 py-3 font-mono text-sm text-ink-900 transition hover:border-grow hover:text-grow"
        >
          <span class="prompt">#</span>
          查看人机对比
        </router-link>

        <a
          href="https://github.com/cxkzai/ai-admissions-platform"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center justify-center gap-2 rounded-lg px-6 py-3 font-mono text-sm text-ink-700 transition hover:text-ink-900"
        >
          <span class="prompt">git</span>
          查看源码 →
        </a>
      </div>
    </div>
  </section>
</template>