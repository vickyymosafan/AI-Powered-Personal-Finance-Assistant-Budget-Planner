'use client'

import { useMutation } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'
import { apiClient } from '@/core/api/client'
import { API_ENDPOINTS } from '@/core/api/endpoints'
import { useAuthStore } from '../stores/auth.store'
import type { AuthResponse, RegisterRequest } from '../types/auth.types'

/**
 * Register mutation hook
 */
export function useRegister() {
  const router = useRouter()
  const { setUser, setTokens } = useAuthStore()

  return useMutation({
    mutationFn: (credentials: RegisterRequest) =>
      apiClient.post<AuthResponse>(API_ENDPOINTS.AUTH.REGISTER, credentials),

    onSuccess: ({ user, tokens }) => {
      setTokens(tokens.access_token, tokens.refresh_token)
      setUser(user)
      router.push('/dashboard')
    },

    onError: (error) => {
      console.error('[useRegister] Error:', error)
    },
  })
}
