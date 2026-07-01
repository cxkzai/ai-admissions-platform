/**
 * 智能体 / 对话 / 工具相关类型定义
 */

export type AgentSlug =
  | 'admission-consultant'
  | 'course-consultant'
  | 'academic-teacher'
  | 'internal-assistant';

export interface Agent {
  id: string;
  slug: AgentSlug;
  name: string;
  description: string;
  icon: string;
  color: 'spark' | 'grow' | 'signal' | 'ink';
  tools: string[];
}

export type Role = 'user' | 'assistant' | 'tool' | 'system';

export interface Citation {
  title: string;
  score: number;
  source: string;
  content?: string;
}

export interface ToolCall {
  id: string;
  name: string;
  arguments: Record<string, unknown>;
}

export interface Message {
  id: string;
  role: Role;
  content: string;
  citations?: Citation[];
  toolCalls?: ToolCall[];
  latencyMs?: number;
  createdAt: string;
}

export interface Conversation {
  id: string;
  agentSlug: AgentSlug;
  channel: 'web' | 'wechat' | 'feishu' | 'mock';
  status: 'active' | 'closed';
  messages: Message[];
}

export interface ChatRequest {
  conversation_id?: string;
  agent_slug: AgentSlug;
  message: string;
  metadata?: Record<string, unknown>;
}

export interface ChatResponse {
  conversation_id: string;
  message_id: string;
  content: string;
  tool_calls?: ToolCall[];
  citations?: Citation[];
  latency_ms: number;
}