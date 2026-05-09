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

export function useTrends() {
  return useQuery({
    queryKey: ['analytics', 'trends'],
    queryFn: () => apiClient.get<TrendsResponse>(API_ENDPOINTS.ANALYTICS.TRENDS),
  })
}

export function useCategories() {
  return useQuery({
    queryKey: ['analytics', 'categories'],
    queryFn: () => apiClient.get<CategoriesResponse>(API_ENDPOINTS.ANALYTICS.CATEGORIES),
  })
}
