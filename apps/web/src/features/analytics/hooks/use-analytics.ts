'use client'

import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/core/api/client'
import { API_ENDPOINTS } from '@/core/api/endpoints'
import type {
  AnalyticsOverviewResponse,
  TrendsResponse,
  CategoriesResponse,
} from '../types/analytics.types'

export function useAnalyticsOverview() {
  return useQuery({
    queryKey: ['analytics', 'overview'],
    queryFn: () => apiClient.get<AnalyticsOverviewResponse>(API_ENDPOINTS.ANALYTICS.OVERVIEW),
  })
}

export function useTrends(year: number = new Date().getFullYear()) {
  return useQuery({
    queryKey: ['analytics', 'trends', year],
    queryFn: () => apiClient.get<TrendsResponse>(`${API_ENDPOINTS.ANALYTICS.TRENDS}?year=${year}`),
  })
}

export function useCategories(
  year: number = new Date().getFullYear(),
  month: number = new Date().getMonth() + 1
) {
  return useQuery({
    queryKey: ['analytics', 'categories', year, month],
    queryFn: () => apiClient.get<CategoriesResponse>(`${API_ENDPOINTS.ANALYTICS.CATEGORIES}?year=${year}&month=${month}`),
  })
}
