import axios from 'axios';
import type {
  Conversation,
  Message,
  ChatRequest,
  ChatResponse,
  PaginatedResponse,
  AIModel,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Conversation APIs
export const conversationApi = {
  list: async (page = 1, pageSize = 20): Promise<PaginatedResponse<Conversation>> => {
    const response = await api.get<PaginatedResponse<Conversation>>('/conversations', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  get: async (id: string): Promise<Conversation> => {
    const response = await api.get<Conversation>(`/conversations/${id}`);
    return response.data;
  },

  create: async (title?: string): Promise<Conversation> => {
    const response = await api.post<Conversation>('/conversations', { title });
    return response.data;
  },

  update: async (id: string, title: string): Promise<Conversation> => {
    const response = await api.put<Conversation>(`/conversations/${id}`, { title });
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/conversations/${id}`);
  },
};

// Message APIs
export const messageApi = {
  list: async (conversationId: string): Promise<Message[]> => {
    const response = await api.get<Message[]>(`/conversations/${conversationId}/messages`);
    return response.data;
  },

  get: async (conversationId: string, messageId: string): Promise<Message> => {
    const response = await api.get<Message>(
      `/conversations/${conversationId}/messages/${messageId}`
    );
    return response.data;
  },
};

// Chat API
export const chatApi = {
  send: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/chat', request);
    return response.data;
  },
};

// Model APIs
export const modelApi = {
  list: async (): Promise<AIModel[]> => {
    const response = await api.get<AIModel[]>('/models');
    return response.data;
  },

  get: async (id: string): Promise<AIModel> => {
    const response = await api.get<AIModel>(`/models/${id}`);
    return response.data;
  },
};

export default api;
