import type { ReactNode } from 'react'

/**
 * Auth route group layout — clean centered page, no sidebar
 * Shared by: /login, /register, /forgot-password
 */
export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <div className="w-full max-w-[400px]">{children}</div>
    </div>
  )
}
