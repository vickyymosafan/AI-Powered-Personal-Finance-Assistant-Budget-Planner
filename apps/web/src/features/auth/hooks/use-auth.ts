import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'
import { authService } from '../services/auth.service'
import { useAuthStore } from '../stores/auth.store'
import type { LoginRequest, RegisterRequest } from '../types/auth.types'

/** Query key factory for auth */
export const authKeys = {
  all: ['auth'] as const,
  me: () => [...authKeys.all, 'me'] as const,
}

/**
 * Hook to get current user
 */
export function useCurrentUser() {
  const { setUser } = useAuthStore()

  return useQuery({
    queryKey: authKeys.me(),
    queryFn: async () => {
      const user = await authService.getMe()
      setUser(user)
      return user
    },
    retry: false,
    staleTime: 5 * 60 * 1000,
  })
}

/**
 * Hook for login mutation
 */
export function useLogin() {
  const queryClient = useQueryClient()
  const router = useRouter()
  const { setTokens, setUser } = useAuthStore()

  return useMutation({
    mutationFn: (data: LoginRequest) => authService.login(data),
    onSuccess: async (tokens) => {
      setTokens(tokens.access_token, tokens.refresh_token)
      const user = await authService.getMe()
      setUser(user)
      queryClient.invalidateQueries({ queryKey: authKeys.all })
      router.push('/')
    },
  })
}

/**
 * Hook for register mutation
 */
export function useRegister() {
  const router = useRouter()
  const { setTokens, setUser } = useAuthStore()

  return useMutation({
    mutationFn: (data: RegisterRequest) => authService.register(data),
    onSuccess: async (tokens) => {
      setTokens(tokens.access_token, tokens.refresh_token)
      const user = await authService.getMe()
      setUser(user)
      router.push('/')
    },
  })
}

/**
 * Hook for logout
 */
export function useLogout() {
  const queryClient = useQueryClient()
  const router = useRouter()
  const { clearAuth } = useAuthStore()

  return useMutation({
    mutationFn: () => authService.logout(),
    onSuccess: () => {
      clearAuth()
      queryClient.clear()
      router.push('/login')
    },
    onError: () => {
      // Force logout even on error
      clearAuth()
      queryClient.clear()
      router.push('/login')
    },
  })
}
