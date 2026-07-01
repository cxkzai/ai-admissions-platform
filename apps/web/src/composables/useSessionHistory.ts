/**
 * 对话历史（sessionStorage 持久化）
 *
 * 设计要点：
 * - 用 sessionStorage 而不是 localStorage：关闭浏览器 tab 后自动清空
 *   （满足"重新登录网页则记录清除"的需求）
 * - 存完整 messages，支持点历史回放
 * - 上限 20 条 session、单条 session 最多 100 条 message、整体容量保护（5MB）
 */

import { ref } from 'vue';
import type { AgentSlug, Message } from '@/types/chat';

export interface Session {
  id: string;
  agent_slug: AgentSlug;
  title: string;          // 首条用户消息前 30 字
  message_count: number;  // 消息总数
  preview: string;        // 最后一条消息前 50 字
  created_at: string;     // ISO 时间
  updated_at: string;     // ISO 时间
  messages: Message[];    // 完整消息（用于点击回放）
}

const STORAGE_KEY = 'edu:session-history';
const MAX_SESSIONS = 20;
const MAX_MESSAGES_PER_SESSION = 100;

function loadFromStorage(): Session[] {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveToStorage(sessions: Session[]): void {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(sessions));
  } catch (e) {
    // 容量超限 / 隐私模式禁用 storage 等
    console.warn('[useSessionHistory] sessionStorage 保存失败（可能容量超限）', e);
  }
}

/** 从 messages 数组中提取 session（深拷贝 messages） */
export function extractSession(
  agent_slug: AgentSlug,
  messages: Message[],
): Omit<Session, 'id' | 'created_at' | 'updated_at'> | null {
  if (messages.length === 0) return null;
  const firstUser = messages.find((m) => m.role === 'user');
  const last = messages[messages.length - 1];
  // 截断过长对话，保护 sessionStorage 容量
  const trimmed =
    messages.length > MAX_MESSAGES_PER_SESSION
      ? messages.slice(-MAX_MESSAGES_PER_SESSION)
      : messages;
  return {
    agent_slug,
    title: firstUser ? firstUser.content.slice(0, 30) : '(空对话)',
    message_count: trimmed.length,
    preview: last ? last.content.slice(0, 50) : '',
    messages: trimmed.map((m) => ({ ...m })),
  };
}

export function useSessionHistory() {
  const history = ref<Session[]>(loadFromStorage());

  function add(
    meta: Omit<Session, 'id' | 'created_at' | 'updated_at'>,
  ): Session {
    const now = new Date().toISOString();
    const session: Session = {
      ...meta,
      id: `sess-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      created_at: now,
      updated_at: now,
    };
    history.value = [session, ...history.value].slice(0, MAX_SESSIONS);
    saveToStorage(history.value);
    return session;
  }

  function getById(id: string): Session | undefined {
    return history.value.find((s) => s.id === id);
  }

  /**
   * 更新已存在的 session（保持 id 和 created_at 不变，刷新 updated_at）
   * 用于"加载历史后继续聊再切走"——把新内容合并回原 session
   */
  function update(
    id: string,
    partial: Partial<Omit<Session, 'id' | 'created_at'>>,
  ): Session | null {
    const idx = history.value.findIndex((s) => s.id === id);
    if (idx === -1) return null;
    const old = history.value[idx];
    const updated: Session = {
      ...old,
      ...partial,
      id: old.id,            // 保持 id 不变
      created_at: old.created_at,  // 保持 created_at 不变
      updated_at: new Date().toISOString(),  // 刷新 updated_at
    };
    // 移到最前（表示最近活跃）
    history.value = [
      updated,
      ...history.value.filter((_, i) => i !== idx),
    ];
    saveToStorage(history.value);
    return updated;
  }

  function remove(id: string): void {
    history.value = history.value.filter((s) => s.id !== id);
    saveToStorage(history.value);
  }

  function clearAll(): void {
    history.value = [];
    saveToStorage(history.value);
  }

  return { history, add, getById, update, remove, clearAll };
}

/** 把 ISO 时间格式化为"X 分钟前"等相对时间 */
export function formatRelativeTime(iso: string): string {
  const now = Date.now();
  const t = new Date(iso).getTime();
  const diff = Math.max(0, now - t);
  const sec = Math.floor(diff / 1000);
  if (sec < 60) return '刚刚';
  const min = Math.floor(sec / 60);
  if (min < 60) return `${min} 分钟前`;
  const hr = Math.floor(min / 60);
  if (hr < 24) return `${hr} 小时前`;
  const day = Math.floor(hr / 24);
  return `${day} 天前`;
}
