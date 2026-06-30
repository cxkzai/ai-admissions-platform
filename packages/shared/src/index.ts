/**
 * 前后端共享类型定义
 */

// ===== 智能体 =====

export type AgentSlug =
  | 'admission-consultant' // 招生顾问
  | 'course-consultant' // 课程顾问
  | 'academic-teacher' // 教务老师
  | 'internal-assistant'; // 内部助手

export interface Agent {
  id: string;
  slug: AgentSlug;
  name: string;
  description: string;
  systemPrompt: string;
  tools: string[];
  model: string;
  temperature: number;
  version: number;
  isActive: boolean;
}

// ===== 对话 =====

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'tool' | 'system';
  content: string;
  toolCalls?: ToolCall[];
  citations?: Citation[];
  createdAt: string;
}

export interface Conversation {
  id: string;
  leadId?: string;
  agentSlug: AgentSlug;
  channel: 'web' | 'wechat' | 'feishu' | 'mock';
  status: 'active' | 'closed';
  messages: Message[];
  createdAt: string;
}

// ===== 工具调用 =====

export interface ToolCall {
  id: string;
  name: string;
  arguments: Record<string, unknown>;
  result?: unknown;
}

// ===== 引用（RAG） =====

export interface Citation {
  title: string;
  score: number;
  source: string;
  content?: string;
}

// ===== 聊天接口 =====

export interface ChatRequest {
  conversationId?: string;
  agentSlug: AgentSlug;
  message: string;
  metadata?: Record<string, unknown>;
}

export interface ChatResponse {
  conversationId: string;
  messageId: string;
  content: string;
  toolCalls?: ToolCall[];
  citations?: Citation[];
  latencyMs: number;
}

// ===== 线索 =====

export interface Lead {
  id: string;
  name?: string;
  phone?: string;
  wechat?: string;
  childAge?: number;
  interestSubject?: string;
  source: 'wechat' | 'web' | 'referral' | 'mock';
  stage: 'new' | 'contacted' | 'audition' | 'won' | 'lost';
  assignedAgentId?: string;
  createdAt: string;
  updatedAt: string;
}

// ===== 知识库 =====

export type KbName =
  | 'courses'
  | 'teachers'
  | 'cases'
  | 'faq'
  | 'scripts'
  | 'sop';

export interface KbDocument {
  id: string;
  kbName: KbName;
  title: string;
  sourcePath: string;
  fileType: string;
  status: 'pending' | 'processing' | 'indexed' | 'failed';
  chunkCount: number;
  createdAt: string;
}

export interface KbChunk {
  id: string;
  docId: string;
  chunkIndex: number;
  content: string;
  metadata: Record<string, unknown>;
}

// ===== 提示词模板 =====

export interface PromptTemplate {
  id: string;
  category: string;
  name: string;
  content: string;
  variables: string[];
  version: number;
  usageCount: number;
  createdAt: string;
}

// ===== API 错误 =====

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}