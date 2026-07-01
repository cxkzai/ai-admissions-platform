/**
 * 对话组合式函数（Composable）
 *
 * 封装消息列表、loading、错误状态、发送逻辑。
 * 后端失败时抛给上层（DemoChatView 显示错误 banner），不再静默用 Mock 兜底。
 */

import { ref } from 'vue';
import type { AgentSlug, Message } from '@/types/chat';
import api from '@/lib/api';

export function useChat(agentSlug: AgentSlug) {
  const messages = ref<Message[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  // 记录最后一次失败的用户消息，用于"重试发送"
  const lastUserMessage = ref<string | null>(null);
  // 标记当前 messages 是否被用户修改过（用于决定切走时是合并到原 session 还是跳过）
  const isDirty = ref(false);

  const send = async (text: string) => {
    if (!text.trim() || loading.value) return;

    const userMsg: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: text,
      createdAt: new Date().toISOString(),
    };
    messages.value.push(userMsg);
    error.value = null;
    loading.value = true;
    isDirty.value = true;  // 用户发了消息 = dirty

    try {
      const response = await api.chat({
        agent_slug: agentSlug,
        message: text,
      });

      messages.value.push({
        id: response.message_id,
        role: 'assistant',
        content: response.content,
        citations: response.citations,
        latencyMs: response.latency_ms,  // 映射到前端内部 Message 的 latencyMs（保持模板兼容性）
        createdAt: new Date().toISOString(),
      });
      lastUserMessage.value = null;  // 成功：清掉重试标记
    } catch (err: unknown) {
      // 提取错误信息，抛给上层显示
      const axiosErr = err as { response?: { data?: { detail?: string } }; message?: string };
      const detail = axiosErr.response?.data?.detail;
      const msg = detail || axiosErr.message || '请求失败，请稍后重试';
      error.value = msg;
      // 移除刚 push 的 user 消息（用户看不到回复，user 消息留着会很奇怪）
      messages.value = messages.value.filter((m) => m.id !== userMsg.id);
      // 记住最后一条失败的消息，供 retry() 使用
      lastUserMessage.value = text;
      console.error('[Chat] 后端调用失败：', msg);
    } finally {
      loading.value = false;
    }
  };

  const retry = async () => {
    if (lastUserMessage.value && !loading.value) {
      await send(lastUserMessage.value);
    }
  };

  const clear = () => {
    messages.value = [];
    error.value = null;
    lastUserMessage.value = null;
    isDirty.value = false;
  };

  const loadMessages = (msgs: Message[]) => {
    messages.value = msgs.map((m) => ({ ...m }));
    error.value = null;
    lastUserMessage.value = null;
    isDirty.value = false;  // 加载历史是干净状态
  };

  return {
    messages,
    loading,
    error,
    isDirty,
    send,
    retry,
    clear,
    loadMessages,
    lastUserMessage,
  };
}