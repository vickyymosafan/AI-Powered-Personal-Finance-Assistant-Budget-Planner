'use client'

import { useCategories } from '../hooks/use-analytics'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'

const COLORS = [
  '#3b82f6', // blue
  '#10b981', // green
  '#f59e0b', // yellow
  '#ef4444', // red
  '#8b5cf6', // purple
  '#ec4899', // pink
  '#06b6d4', // cyan
  '#f97316', // orange
]

export function CategoriesChart() {
  const { data, isLoading, error } = useCategories()

  if (isLoading) {
    return (
      <Card className="w-full h-[400px] flex items-center justify-center">
        <div className="text-muted-foreground animate-pulse">Memuat grafik...</div>
      </Card>
    )
  }

  if (error || !data) {
    return (
      <Card className="w-full h-[400px] flex items-center justify-center">
        <div className="text-destructive">Gagal memuat data kategori.</div>
      </Card>
    )
  }

  return (
    <Card className="w-full glassmorphism">
      <CardHeader>
        <CardTitle className="text-lg font-semibold">Pengeluaran per Kategori</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data.categories}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="amount"
                nameKey="category"
                label={(props: unknown) => {
                  const p = props as { payload: { category: string; percentage: number } }
                  return `${p.payload.category} (${p.payload.percentage.toFixed(1)}%)`
                }}
              >
                {data.categories.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(0, 0, 0, 0.8)',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#fff'
                }}
                itemStyle={{ color: '#fff' }}
                formatter={(value: unknown) => {
                  if (value === undefined || value === null) return ''
                  if (Array.isArray(value)) return `Rp ${Number(value[0]).toLocaleString()}`
                  return `Rp ${Number(value).toLocaleString()}`
                }}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}
