'use client'

import type { ReactNode } from 'react'
import { QueryProvider } from './query-provider'
import { ThemeProvider } from './theme-provider'

interface AppProvidersProps {
  children: ReactNode
}

/**
 * Composed application providers
 * Order matters: outermost provider wraps innermost
 */
export function AppProviders({ children }: AppProvidersProps) {
  return (
    <QueryProvider>
      <ThemeProvider defaultTheme="system">
        {children}
      </ThemeProvider>
    </QueryProvider>
  )
}
