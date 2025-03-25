import { useState, useCallback } from 'react';
import { useAuthStore } from '@/store/authStore';
import { useNotificationStore } from '@/store/notificationStore';

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  body?: any;
  headers?: Record<string, string>;
  requiresAuth?: boolean;
}

interface ApiState<T> {
  data: T | null;
  error: Error | null;
  isLoading: boolean;
}

export function useApi<T = any>(endpoint: string, defaultOptions: ApiOptions = {}) {
  const [state, setState] = useState<ApiState<T>>({
    data: null,
    error: null,
    isLoading: false,
  });

  const token = useAuthStore((state) => state.token);
  const addNotification = useNotificationStore((state) => state.addNotification);

  const execute = useCallback(
    async (options: ApiOptions = {}) => {
      const {
        method = 'GET',
        body,
        headers = {},
        requiresAuth = true,
      } = { ...defaultOptions, ...options };

      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      try {
        const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'https://api.docmatrixai.com';
        const url = `${baseUrl}${endpoint}`;

        const requestHeaders: Record<string, string> = {
          'Content-Type': 'application/json',
          ...headers,
        };

        if (requiresAuth && token) {
          requestHeaders.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(url, {
          method,
          headers: requestHeaders,
          body: body ? JSON.stringify(body) : undefined,
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || 'An error occurred');
        }

        const data = await response.json();
        setState({ data, error: null, isLoading: false });
        return data;
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'An error occurred';
        setState({ data: null, error: error as Error, isLoading: false });
        
        addNotification({
          type: 'error',
          message: errorMessage,
        });

        throw error;
      }
    },
    [endpoint, token, addNotification, defaultOptions]
  );

  return {
    ...state,
    execute,
  };
} 