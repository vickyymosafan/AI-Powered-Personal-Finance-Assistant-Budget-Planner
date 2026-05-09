/**
 * Auth domain types
 * No Next.js imports allowed in this layer
 */

export interface User {
  id: string
  email: string
  full_name: string
  avatar_url: string | null
  currency: string
  locale: string
  created_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterPayload {
  email: string
  password: string
  full_name: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: 'bearer'
  expires_in: number
}

export interface AuthResponse {
  user: User
  tokens: AuthTokens
}
