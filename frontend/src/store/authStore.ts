import { create } from 'zustand';
import { apiService } from '../services/api';

interface User {
  id: string;
  email: string;
  full_name?: string;
  created_at: string;
  is_active: boolean;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  isLoading: false,
  error: null,

  login: async (email: string, password: string) => {
    try {
      set({ isLoading: true, error: null });
      await apiService.login(email, password);
      const user = await apiService.getMe();
      set({
        user,
        token: localStorage.getItem('token'),
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Login failed',
        isLoading: false,
      });
      throw error;
    }
  },

  register: async (email: string, password: string, fullName?: string) => {
    try {
      set({ isLoading: true, error: null });
      await apiService.register(email, password, fullName);
      await apiService.login(email, password);
      const user = await apiService.getMe();
      set({
        user,
        token: localStorage.getItem('token'),
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Registration failed',
        isLoading: false,
      });
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    set({
      user: null,
      token: null,
      isAuthenticated: false,
      error: null,
    });
  },

  fetchUser: async () => {
    try {
      set({ isLoading: true });
      const user = await apiService.getMe();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (error) {
      set({ isAuthenticated: false, isLoading: false });
      localStorage.removeItem('token');
    }
  },

  clearError: () => set({ error: null }),
}));
