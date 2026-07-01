<script setup lang="ts">
</script>

<template>
  <main class="flex min-h-screen items-center justify-center bg-ink-50">
    <div class="container-page text-center">
      <div class="mb-6 font-mono text-sm text-ink-500">
         ls /404
      </div>
      <h1 class="mb-4 font-display text-mega font-bold text-ink-900">
        404
      </h1>
      <p class="mb-8 font-mono text-sm text-ink-700">
        <span class="prompt">#</span> path not found
      </p>
      <router-link
        to="/"
        class="inline-flex items-center gap-2 rounded-lg border border-spark bg-spark px-6 py-3 font-mono text-sm text-white transition hover:bg-spark-dark hover:text-ink-900"
      >
        <span class="prompt text-white group-hover:text-ink-900">$</span>
        cd ~
      </router-link>
    </div>
  </main>
</template>