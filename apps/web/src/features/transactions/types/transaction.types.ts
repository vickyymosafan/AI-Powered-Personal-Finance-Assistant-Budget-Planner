import type { TransactionCategory, TransactionType } from '@/shared/constants/app.constants'

export interface Transaction {
  id: string
  user_id: string
  type: TransactionType
  category: TransactionCategory
  amount: number
  description: string
  date: string
  notes: string | null
  created_at: string
  updated_at: string
}

export interface TransactionSummary {
  total_income: number
  total_expense: number
  net: number
  period: string
}

export interface CreateTransactionPayload {
  type: TransactionType
  category: TransactionCategory
  amount: number
  description: string
  date: string
  notes?: string
}

export type UpdateTransactionPayload = Partial<CreateTransactionPayload>
