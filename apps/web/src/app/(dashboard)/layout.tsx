import type { ReactNode } from 'react'
import { AuthGuard } from '@/core/guards/auth-guard'

/**
 * Dashboard route group layout — protected shell with sidebar + navbar
 * All routes inside require authentication
 */
export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <AuthGuard>
      <div className="flex min-h-screen bg-background">
        {/* Sidebar — will be replaced with full Sidebar component */}
        <aside className="hidden w-64 shrink-0 border-r border-border bg-sidebar lg:flex lg:flex-col">
          <div className="flex h-16 items-center border-b border-sidebar-border px-6">
            <span className="text-lg font-bold text-sidebar-foreground">
              FinanceAI
            </span>
          </div>
          <nav className="flex-1 overflow-y-auto p-4">
            {/* DashboardNav will be implemented */}
          </nav>
        </aside>

        {/* Main content area */}
        <div className="flex flex-1 flex-col overflow-hidden">
          {/* Top navbar — will be replaced with full Navbar component */}
          <header className="flex h-16 shrink-0 items-center border-b border-border bg-background px-6">
            <div className="ml-auto flex items-center gap-4">
              {/* UserMenu, ThemeToggle will be added here */}
            </div>
          </header>

          <main className="flex-1 overflow-y-auto p-6">{children}</main>
        </div>
      </div>
    </AuthGuard>
  )
}
