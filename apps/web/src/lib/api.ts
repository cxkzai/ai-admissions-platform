/**
 * API 客户端
 *
 * 与 FastAPI 后端的对话接口。
 * 开发时通过 Vite proxy 转发到 http://localhost:8000
 */

import axios, { type AxiosInstance } from 'axios';
import type { ChatRequest, ChatResponse } from '@/types/chat';

const http: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 60_000,
  headers: { 'Content-Type': 'application/json' },
});

http.interceptors.response.use(
  (r) => r,
  (err) => {
    console.error('[API Error]', err.response?.data || err.message);
    return Promise.reject(err);
  },
);

export const api = {
  /** 发送消息给智能体 */
  async chat(req: ChatRequest): Promise<ChatResponse> {
    const { data } = await http.post<ChatResponse>('/chat/message', req);
    return data;
  },

  /** 健康检查 */
  async health(): Promise<{ status: string }> {
    const { data } = await http.get('/health');
    return data;
  },

  /** 获取智能体列表 */
  async listAgents(): Promise<unknown[]> {
    const { data } = await http.get('/admin/agents');
    return data;
  },
};

export default api;