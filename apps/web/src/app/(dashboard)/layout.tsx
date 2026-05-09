import type { ReactNode } from 'react'
import { AuthGuard } from '@/core/guards/auth-guard'
import { DashboardSidebar } from '@/features/dashboard/components/DashboardSidebar'
import { DashboardTopbar } from '@/features/dashboard/components/DashboardTopbar'

/**
 * Dashboard route group layout — protected shell with sidebar + navbar
 * All routes inside require authentication
 */
export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <AuthGuard>
      <div className="flex min-h-screen bg-background">
        <DashboardSidebar />

        {/* Main content area */}
        <div className="flex flex-1 flex-col overflow-hidden">
          <DashboardTopbar />

          <main className="flex-1 overflow-y-auto p-6">{children}</main>
        </div>
      </div>
    </AuthGuard>
  )
}
