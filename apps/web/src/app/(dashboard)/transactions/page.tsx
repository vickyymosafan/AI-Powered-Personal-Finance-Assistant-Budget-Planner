import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Transactions',
  description: 'Manage and track your transactions',
}

export default function TransactionsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Transactions</h1>
        <p className="text-sm text-muted-foreground">
          Track and manage all your financial transactions
        </p>
      </div>
      {/* TransactionList, TransactionFilters components will go here */}
    </div>
  )
}
