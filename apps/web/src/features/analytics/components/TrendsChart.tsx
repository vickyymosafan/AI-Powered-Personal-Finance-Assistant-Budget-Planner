'use client'

import { useTrends } from '../hooks/use-analytics'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'
import { Bot } from 'lucide-react'

export function TrendsChart() {
  const { data, isLoading, error } = useTrends()

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
        <div className="text-destructive">Gagal memuat data tren.</div>
      </Card>
    )
  }

  return (
    <Card className="w-full glassmorphism">
      <CardHeader>
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          Tren Keuangan
          <Bot className="h-4 w-4 text-primary" />
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={data.trends}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey="period" 
                stroke="#888888" 
                fontSize={12} 
                tickLine={false} 
                axisLine={false} 
              />
              <YAxis 
                stroke="#888888" 
                fontSize={12} 
                tickLine={false} 
                axisLine={false}
                tickFormatter={(value) => `Rp ${value.toLocaleString()}`}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(0, 0, 0, 0.8)', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff'
                }} 
                labelStyle={{ color: '#fff' }}
                itemStyle={{ color: '#fff' }}
                formatter={(value: unknown) => {
                  if (value === undefined || value === null) return ''
                  if (Array.isArray(value)) return `Rp ${Number(value[0]).toLocaleString()}`
                  return `Rp ${Number(value).toLocaleString()}`
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="income"
                name="Pemasukan"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
              <Line
                type="monotone"
                dataKey="expense"
                name="Pengeluaran"
                stroke="#ef4444"
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}
