import type { BudgetPeriod, TransactionCategory } from '@/shared/constants/app.constants'

export interface Budget {
  id: string
  user_id: string
  category: TransactionCategory
  limit_amount: number
  period: BudgetPeriod
  start_date: string
  end_date: string | null
  created_at: string
  updated_at: string
}

export interface BudgetProgress extends Budget {
  spent_amount: number
  remaining_amount: number
  percentage_used: number
  is_exceeded: boolean
}

export interface CreateBudgetPayload {
  category: TransactionCategory
  limit_amount: number
  period: BudgetPeriod
  start_date: string
}

export type UpdateBudgetPayload = Partial<CreateBudgetPayload>
