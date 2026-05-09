'use client'

import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/core/api/client'
import { API_ENDPOINTS } from '@/core/api/endpoints'
import { QUERY_KEYS } from '@/shared/constants/app.constants'
import type { ApiListResponse } from '@/shared/types/api.types'
import type { Transaction, TransactionSummary } from '../types/transaction.types'
import type { PaginationParams } from '@/shared/types/api.types'

type TransactionFilters = PaginationParams & {
  type?: string
  category?: string
  date_from?: string
  date_to?: string
}

/**
 * Paginated transactions list query
 */
export function useTransactions(filters: TransactionFilters = {}) {
  return useQuery({
    queryKey: [QUERY_KEYS.TRANSACTIONS, filters],
    queryFn: ({ signal }) =>
      apiClient.get<ApiListResponse<Transaction>>(API_ENDPOINTS.TRANSACTIONS.BASE, {
        params: {
          page: String(filters.page ?? 1),
          per_page: String(filters.per_page ?? 20),
          ...(filters.type && { type: filters.type }),
          ...(filters.category && { category: filters.category }),
          ...(filters.date_from && { date_from: filters.date_from }),
          ...(filters.date_to && { date_to: filters.date_to }),
          ...(filters.sort_by && { sort_by: filters.sort_by }),
          ...(filters.sort_order && { sort_order: filters.sort_order }),
        },
        signal,
      }),
    staleTime: 30 * 1000,
  })
}

/**
 * Transaction summary (income/expense totals)
 */
export function useTransactionSummary() {
  return useQuery({
    queryKey: [QUERY_KEYS.TRANSACTIONS, 'summary'],
    queryFn: ({ signal }) =>
      apiClient.get<TransactionSummary>(API_ENDPOINTS.TRANSACTIONS.SUMMARY, { signal }),
    staleTime: 60 * 1000,
  })
}
