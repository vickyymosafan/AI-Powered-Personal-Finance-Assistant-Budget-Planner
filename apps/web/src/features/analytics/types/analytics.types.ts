export interface AnalyticsOverviewResponse {
  total_income: number
  total_expense: number
  net_balance: number
  active_goals_count: number
  completed_goals_count: number
}

export interface TrendDataPoint {
  period: string
  income: number
  expense: number
}

export interface TrendsResponse {
  trends: TrendDataPoint[]
}

export interface CategoryDataPoint {
  category: string
  amount: number
  percentage: number
}

export interface CategoriesResponse {
  categories: CategoryDataPoint[]
}
