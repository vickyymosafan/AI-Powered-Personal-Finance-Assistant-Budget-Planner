/**
 * API response and error types
 * Shared contract between frontend and backend
 */

export interface ApiResponse<T> {
  data: T
  message?: string
  meta?: PaginationMeta
}

export interface ApiError {
  status: number
  message: string
  detail: string | Record<string, string[]> | null
}

export interface PaginationMeta {
  page: number
  per_page: number
  total: number
  total_pages: number
}

export interface PaginationParams {
  page?: number
  per_page?: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

export interface ApiListResponse<T> {
  data: T[]
  meta: PaginationMeta
}
