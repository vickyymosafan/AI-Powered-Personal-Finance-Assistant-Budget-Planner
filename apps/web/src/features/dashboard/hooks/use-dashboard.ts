'use client'

import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/core/api/client'
import { API_ENDPOINTS } from '@/core/api/endpoints'
import { QUERY_KEYS } from '@/shared/constants/app.constants'

export interface DashboardOverview {
  balance: number
  monthly_income: number
  monthly_expense: number
  savings_rate: number
  budget_alerts: number
  recent_transactions: Array<{
    id: string
    description: string
    amount: number
    type: 'income' | 'expense'
    date: string
  }>
}

/**
 * Dashboard overview data — combined summary for the main dashboard
 */
export function useDashboard() {
  return useQuery({
    queryKey: [QUERY_KEYS.DASHBOARD],
    queryFn: ({ signal }) =>
      apiClient.get<DashboardOverview>(API_ENDPOINTS.ANALYTICS.OVERVIEW, { signal }),
    staleTime: 60 * 1000,
    refetchInterval: 5 * 60 * 1000, // Auto-refresh every 5 minutes
  })
}
