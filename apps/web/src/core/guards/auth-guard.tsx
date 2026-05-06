'use client'

import { useEffect, type ReactNode } from 'react'
import { useRouter } from 'next/navigation'

/**
 * Auth guard — protects routes requiring authentication
 * Redirects to login if no token found
 */
interface AuthGuardProps {
  children: ReactNode
  fallbackUrl?: string
}

export function AuthGuard({
  children,
  fallbackUrl = '/login',
}: AuthGuardProps) {
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.replace(fallbackUrl)
    }
  }, [router, fallbackUrl])

  // Render children only if token exists
  const token =
    typeof window !== 'undefined'
      ? localStorage.getItem('access_token')
      : null

  if (!token) return null

  return <>{children}</>
}
