/**
 * Centralized API endpoint definitions
 * Single source of truth for all backend routes
 */
export const API_ENDPOINTS = {
  // Auth
  AUTH: {
    LOGIN: '/api/v1/auth/login',
    REGISTER: '/api/v1/auth/register',
    REFRESH: '/api/v1/auth/refresh',
    ME: '/api/v1/auth/me',
    LOGOUT: '/api/v1/auth/logout',
  },

  // Transactions
  TRANSACTIONS: {
    BASE: '/api/v1/transactions',
    BY_ID: (id: string) => `/api/v1/transactions/${id}`,
    SUMMARY: '/api/v1/transactions/summary',
  },

  // Budgets
  BUDGETS: {
    BASE: '/api/v1/budgets',
    BY_ID: (id: string) => `/api/v1/budgets/${id}`,
    PROGRESS: '/api/v1/budgets/progress',
  },

  // Analytics
  ANALYTICS: {
    OVERVIEW: '/api/v1/analytics/overview',
    SPENDING: '/api/v1/analytics/spending',
    TRENDS: '/api/v1/analytics/trends',
    CATEGORIES: '/api/v1/analytics/categories',
  },

  // AI Assistant
  AI: {
    CHAT: '/api/v1/ai/chat',
    INSIGHTS: '/api/v1/ai/insights',
    ADVICE: '/api/v1/ai/advice',
  },
} as const
