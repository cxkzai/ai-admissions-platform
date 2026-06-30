import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: 'AI-Admissions · 教培 AI 招生顾问' },
  },
  {
    path: '/demo/chat',
    name: 'demo-chat',
    component: () => import('@/views/DemoChatView.vue'),
    meta: { title: '智能体对话 · Demo' },
  },
  {
    path: '/demo/compare',
    name: 'demo-compare',
    component: () => import('@/views/DemoCompareView.vue'),
    meta: { title: '人机对比 · Demo' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
    meta: { title: '404 · 路径不存在' },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0, behavior: 'smooth' }),
});

router.beforeEach((to) => {
  const title = (to.meta.title as string) || 'AI-Admissions Platform';
  document.title = title;
});

export default router;