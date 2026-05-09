import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Analytics',
  description: 'Deep insights into your financial data',
}

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Analytics</h1>
        <p className="text-sm text-muted-foreground">
          Visualize spending trends and financial patterns
        </p>
      </div>
      {/* SpendingChart, TrendsChart, CategoryBreakdown components will go here */}
    </div>
  )
}
