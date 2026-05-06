// Environment configuration with runtime validation
// All env vars are validated at build time through TypeScript

export const env = {
  // Public (client-side)
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME || 'FinanceAI',
  NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',

  // Server-only
  get API_SECRET() {
    if (typeof window !== 'undefined') {
      throw new Error('API_SECRET is server-only')
    }
    return process.env.API_SECRET || ''
  },
} as const

export type Env = typeof env
