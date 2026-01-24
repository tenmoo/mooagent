import { create } from 'zustand';
import { apiService } from '../services/api';

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  selectedModel: string | null;
  sendMessage: (content: string, model?: string) => Promise<void>;
  clearMessages: () => void;
  clearError: () => void;
  setSelectedModel: (model: string) => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isLoading: false,
  error: null,
  selectedModel: null,

  sendMessage: async (content: string, model?: string) => {
    try {
      set({ isLoading: true, error: null });

      // Add user message
      const userMessage: Message = {
        role: 'user',
        content,
        timestamp: new Date(),
      };
      set((state) => ({ messages: [...state.messages, userMessage] }));

      // Get conversation history
      const conversationHistory = get().messages.map((msg) => ({
        role: msg.role,
        content: msg.content,
      }));

      // Use provided model or selected model from state
      const modelToUse = model || get().selectedModel || undefined;
      console.log('📤 Sending message with model:', modelToUse);

      // Send to API
      const response = await apiService.sendMessage(content, conversationHistory, modelToUse);

      // Add assistant response
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };
      set((state) => ({
        messages: [...state.messages, assistantMessage],
        isLoading: false,
      }));
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Failed to send message',
        isLoading: false,
      });
      throw error;
    }
  },

  clearMessages: () => set({ messages: [], error: null }),

  clearError: () => set({ error: null }),

  setSelectedModel: (model: string) => set({ selectedModel: model }),
}));
