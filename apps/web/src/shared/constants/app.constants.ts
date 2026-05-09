/**
 * App-wide constants
 * No side effects — pure config values
 */

export const APP_NAME = 'FinanceAI'

export const TRANSACTION_CATEGORIES = [
  'Makanan & Minuman',
  'Transportasi',
  'Belanja',
  'Tagihan & Utilitas',
  'Hiburan',
  'Kesehatan',
  'Pendidikan',
  'Perumahan',
  'Investasi',
  'Tabungan',
  'Gaji',
  'Bonus',
  'Freelance',
  'Lainnya',
] as const

export type TransactionCategory = (typeof TRANSACTION_CATEGORIES)[number]

export const TRANSACTION_TYPES = ['income', 'expense', 'transfer'] as const
export type TransactionType = (typeof TRANSACTION_TYPES)[number]

export const BUDGET_PERIODS = ['weekly', 'monthly', 'yearly'] as const
export type BudgetPeriod = (typeof BUDGET_PERIODS)[number]

export const NAV_ITEMS = [
  { label: 'Dashboard', href: '/dashboard', icon: 'layout-dashboard' },
  { label: 'Transactions', href: '/transactions', icon: 'arrow-left-right' },
  { label: 'Budgets', href: '/budgets', icon: 'wallet' },
  { label: 'Analytics', href: '/analytics', icon: 'bar-chart-2' },
  { label: 'AI Assistant', href: '/ai-assistant', icon: 'bot' },
] as const

export const PAGINATION_DEFAULTS = {
  PAGE: 1,
  PER_PAGE: 20,
  MAX_PER_PAGE: 100,
} as const

export const QUERY_KEYS = {
  TRANSACTIONS: 'transactions',
  BUDGETS: 'budgets',
  ANALYTICS: 'analytics',
  DASHBOARD: 'dashboard',
  AI_CHAT: 'ai-chat',
  AUTH_ME: 'auth-me',
} as const

export const LOCAL_STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  THEME: 'theme',
} as const
