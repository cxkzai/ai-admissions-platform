/**
 * 对话组合式函数（Composable）
 *
 * 封装消息列表、loading、发送逻辑。
 * 提供 Mock 模式（后端未启动时）。
 */

import { ref } from 'vue';
import type { AgentSlug, Message } from '@/types/chat';
import api from '@/lib/api';

const MOCK_RESPONSES: Record<AgentSlug, string[]> = {
  'admission-consultant': [
    `> 您好，欢迎咨询码力星编程 👋

我是 AI 招生顾问小码，10 年教培招生经验。

方便问一下：
  1. 孩子几岁了？
  2. 有没有接触过编程？
  3. 主要是想培养兴趣，还是准备比赛？`,
  ],
  'course-consultant': [
    `> 好的，我来帮您对比下 Scratch 和 Python。

  [courses/scratch.md]
  - 适合 8-10 岁，图形化拖拽
  - 48 课时，学完能独立做小游戏
  - 原价 ¥6,800，限时 ¥5,800

  [courses/python.md]
  - 适合 10-12 岁，代码编程
  - 60 课时，含 5 个实战项目
  - 原价 ¥8,800，限时 ¥7,800

您家孩子的年龄和基础情况是怎样的？我可以更精准地推荐。`,
  ],
  'academic-teacher': [
    `> 这是试听后的跟进话术建议：

【24h 内】
"XX 妈妈您好，孩子试听表现得 [具体亮点]，我们老师反馈 [优点]..."

【3 天后】
"上次试听之后，我们教研组针对孩子的表现做了 [个性化建议]..."

【7 天后（最后窗口）】
"XX 妈妈，试听专属优惠还剩 3 天..."

要我把哪个阶段的文案展开吗？`,
  ],
  'internal-assistant': [
    `> 找到了 SOP，整理如下：

## 试听课前准备清单

- [ ] 教室设备检查（投影/iPad/网络）
- [ ] 备课资料打印（含家长版）
- [ ] 学员档案调取
- [ ] 家长接送指引
- [ ] 课前 15 分钟接待流程演练
- [ ] 应急联系方式确认

参考文档：sop/audition-prep.md`,
  ],
};

export function useChat(agentSlug: AgentSlug) {
  const messages = ref<Message[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

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

    try {
      // 尝试调用真实 API
      const response = await api.chat({
        agentSlug,
        message: text,
      });

      messages.value.push({
        id: response.messageId,
        role: 'assistant',
        content: response.content,
        citations: response.citations,
        latencyMs: response.latencyMs,
        createdAt: new Date().toISOString(),
      });
    } catch (err) {
      // 后端未启动时使用 Mock 模式
      console.warn('[Chat] 后端不可用，进入 Mock 模式', err);
      await new Promise((r) => setTimeout(r, 800));

      const mockContent =
        MOCK_RESPONSES[agentSlug]?.[0] || '> 这是一个 Mock 回复，完整功能待后端联调后启用。';

      messages.value.push({
        id: `mock-${Date.now()}`,
        role: 'assistant',
        content: mockContent,
        latencyMs: 800,
        createdAt: new Date().toISOString(),
      });
    } finally {
      loading.value = false;
    }
  };

  const clear = () => {
    messages.value = [];
    error.value = null;
  };

  return {
    messages,
    loading,
    error,
    send,
    clear,
  };
}