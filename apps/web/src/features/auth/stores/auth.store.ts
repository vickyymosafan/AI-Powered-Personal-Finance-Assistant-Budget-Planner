import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type { User } from '../types/auth.types'

interface AuthStore {
  user: User | null
  isAuthenticated: boolean

  // Actions
  setUser: (user: User) => void
  clearAuth: () => void
  setTokens: (accessToken: string, refreshToken: string) => void
}

export const useAuthStore = create<AuthStore>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        isAuthenticated: false,

        setUser: (user) =>
          set({ user, isAuthenticated: true }, undefined, 'auth/setUser'),

        clearAuth: () => {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          set(
            { user: null, isAuthenticated: false },
            undefined,
            'auth/clearAuth'
          )
        },

        setTokens: (accessToken, refreshToken) => {
          localStorage.setItem('access_token', accessToken)
          localStorage.setItem('refresh_token', refreshToken)
        },
      }),
      {
        name: 'auth-storage',
        partialize: (state) => ({ user: state.user }),
      }
    ),
    { name: 'auth-store' }
  )
)
