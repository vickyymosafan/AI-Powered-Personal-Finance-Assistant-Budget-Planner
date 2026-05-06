import { apiClient } from '@/core/api/client'
import { API_ENDPOINTS } from '@/core/api/endpoints'
import type {
  AuthTokens,
  LoginRequest,
  RegisterRequest,
  User,
} from '../types/auth.types'

/**
 * Auth API service — all auth-related HTTP calls
 */
export const authService = {
  async login(data: LoginRequest): Promise<AuthTokens> {
    return apiClient.post<AuthTokens>(API_ENDPOINTS.AUTH.LOGIN, data)
  },

  async register(data: RegisterRequest): Promise<AuthTokens> {
    return apiClient.post<AuthTokens>(API_ENDPOINTS.AUTH.REGISTER, data)
  },

  async getMe(): Promise<User> {
    return apiClient.get<User>(API_ENDPOINTS.AUTH.ME)
  },

  async refreshToken(refreshToken: string): Promise<AuthTokens> {
    return apiClient.post<AuthTokens>(API_ENDPOINTS.AUTH.REFRESH, {
      refresh_token: refreshToken,
    })
  },

  async logout(): Promise<void> {
    return apiClient.post(API_ENDPOINTS.AUTH.LOGOUT)
  },
}
