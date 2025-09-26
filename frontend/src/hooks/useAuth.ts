import React from 'react';
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authApi } from '@/services/api';
import type { User, LoginRequest } from '@/types';

interface AuthStore {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
  register: (userData: { email: string; password: string; name?: string }) => Promise<void>;
  getProfile: () => Promise<void>;
  updateProfile: (userData: Partial<User>) => Promise<void>;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (credentials: LoginRequest) => {
        try {
          set({ isLoading: true });
          const response = await authApi.login(credentials);
          const token = response.access_token;
          
          // Сохраняем токен
          localStorage.setItem('token', token);
          
          // Получаем профиль пользователя
          const user = await authApi.getProfile();
          
          set({
            token,
            user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      logout: () => {
        localStorage.removeItem('token');
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },

      register: async (userData: { email: string; password: string; name?: string }) => {
        try {
          set({ isLoading: true });
          await authApi.register(userData);
          set({ isLoading: false });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      getProfile: async () => {
        try {
          const user = await authApi.getProfile();
          set({ user });
        } catch (error) {
          console.error('Failed to get profile:', error);
          // Если не удалось получить профиль, выходим
          get().logout();
        }
      },

      updateProfile: async (userData: Partial<User>) => {
        try {
          const user = await authApi.updateProfile(userData);
          set({ user });
        } catch (error) {
          throw error;
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

export const useAuth = () => {
  const store = useAuthStore();
  
  // Проверяем токен при инициализации
  React.useEffect(() => {
    const token = localStorage.getItem('token');
    if (token && !store.user) {
      store.getProfile();
    }
  }, []);

  return store;
};

// Экспорт для удобства
export default useAuth;
