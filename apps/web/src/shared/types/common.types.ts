/**
 * Common types used across multiple features
 */

export type ID = string

export interface BaseEntity {
  id: ID
  created_at: string
  updated_at: string
}

export interface SelectOption {
  label: string
  value: string
}

export type DateRange = {
  from: Date
  to: Date
}

export type Currency = 'IDR' | 'USD' | 'EUR' | 'GBP'

export type TransactionType = 'income' | 'expense'

export type BudgetPeriod = 'daily' | 'weekly' | 'monthly' | 'yearly'
