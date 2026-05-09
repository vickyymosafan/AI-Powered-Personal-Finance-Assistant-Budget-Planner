import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Budgets',
  description: 'Set and monitor your budget goals',
}

export default function BudgetsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Budgets</h1>
        <p className="text-sm text-muted-foreground">
          Set spending limits and track your progress
        </p>
      </div>
      {/* BudgetList, BudgetProgress components will go here */}
    </div>
  )
}
