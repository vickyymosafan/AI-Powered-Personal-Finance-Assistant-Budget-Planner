import { env } from '@/core/config/env'
import type { ApiError, ApiResponse } from '@/shared/types/api.types'

type RequestConfig = {
  headers?: Record<string, string>
  params?: Record<string, string>
  signal?: AbortSignal
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private getHeaders(custom?: Record<string, string>): HeadersInit {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...custom,
    }

    // Inject auth token if available (client-side only)
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token')
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
    }

    return headers
  }

  private buildUrl(path: string, params?: Record<string, string>): string {
    const url = new URL(`${this.baseUrl}${path}`)
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        url.searchParams.set(key, value)
      })
    }
    return url.toString()
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error: ApiError = {
        status: response.status,
        message: response.statusText,
        detail: null,
      }

      try {
        const body = await response.json()
        error.message = body.message || body.detail || response.statusText
        error.detail = body.detail || null
      } catch {
        // Response body is not JSON
      }

      throw error
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return null as T
    }

    return response.json()
  }

  async get<T>(path: string, config?: RequestConfig): Promise<T> {
    const url = this.buildUrl(path, config?.params)
    const response = await fetch(url, {
      method: 'GET',
      headers: this.getHeaders(config?.headers),
      signal: config?.signal,
    })
    return this.handleResponse<T>(response)
  }

  async post<T>(path: string, body?: unknown, config?: RequestConfig): Promise<T> {
    const url = this.buildUrl(path, config?.params)
    const response = await fetch(url, {
      method: 'POST',
      headers: this.getHeaders(config?.headers),
      body: body ? JSON.stringify(body) : undefined,
      signal: config?.signal,
    })
    return this.handleResponse<T>(response)
  }

  async put<T>(path: string, body?: unknown, config?: RequestConfig): Promise<T> {
    const url = this.buildUrl(path, config?.params)
    const response = await fetch(url, {
      method: 'PUT',
      headers: this.getHeaders(config?.headers),
      body: body ? JSON.stringify(body) : undefined,
      signal: config?.signal,
    })
    return this.handleResponse<T>(response)
  }

  async patch<T>(path: string, body?: unknown, config?: RequestConfig): Promise<T> {
    const url = this.buildUrl(path, config?.params)
    const response = await fetch(url, {
      method: 'PATCH',
      headers: this.getHeaders(config?.headers),
      body: body ? JSON.stringify(body) : undefined,
      signal: config?.signal,
    })
    return this.handleResponse<T>(response)
  }

  async delete<T>(path: string, config?: RequestConfig): Promise<T> {
    const url = this.buildUrl(path, config?.params)
    const response = await fetch(url, {
      method: 'DELETE',
      headers: this.getHeaders(config?.headers),
      signal: config?.signal,
    })
    return this.handleResponse<T>(response)
  }
}

// Singleton instance
export const apiClient = new ApiClient(env.NEXT_PUBLIC_API_URL)
