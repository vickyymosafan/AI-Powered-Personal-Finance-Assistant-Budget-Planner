'use client'

import { useMutation } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'
import { apiClient } from '@/core/api/client'
import { API_ENDPOINTS } from '@/core/api/endpoints'
import { useAuthStore } from '../stores/auth.store'
import type { AuthResponse, LoginCredentials } from '../types/auth.types'

/**
 * Login mutation hook
 * Handles: API call → token storage → auth store update → redirect
 */
export function useLogin() {
  const router = useRouter()
  const { setUser, setTokens } = useAuthStore()

  return useMutation({
    mutationFn: (credentials: LoginCredentials) =>
      apiClient.post<AuthResponse>(API_ENDPOINTS.AUTH.LOGIN, credentials),

    onSuccess: ({ user, tokens }) => {
      setTokens(tokens.access_token, tokens.refresh_token)
      setUser(user)
      router.push('/dashboard')
    },

    onError: (error) => {
      console.error('[useLogin] Error:', error)
    },
  })
}
