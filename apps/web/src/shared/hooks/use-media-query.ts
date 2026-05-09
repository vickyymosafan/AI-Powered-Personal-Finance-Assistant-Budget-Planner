'use client'

import { useCallback, useSyncExternalStore } from 'react'

type Breakpoint = 'sm' | 'md' | 'lg' | 'xl' | '2xl'

const BREAKPOINTS: Record<Breakpoint, string> = {
  sm: '(min-width: 640px)',
  md: '(min-width: 768px)',
  lg: '(min-width: 1024px)',
  xl: '(min-width: 1280px)',
  '2xl': '(min-width: 1536px)',
}

/**
 * Responsive breakpoint hook
 * @param breakpoint - Tailwind breakpoint name or custom media query
 */
export function useMediaQuery(query: Breakpoint | string): boolean {
  const resolvedQuery =
    query in BREAKPOINTS ? BREAKPOINTS[query as Breakpoint] : query

  const subscribe = useCallback(
    (callback: () => void) => {
      if (typeof window === 'undefined') return () => {}
      const media = window.matchMedia(resolvedQuery)
      media.addEventListener('change', callback)
      return () => media.removeEventListener('change', callback)
    },
    [resolvedQuery]
  )

  const getSnapshot = useCallback(() => {
    if (typeof window === 'undefined') return false
    return window.matchMedia(resolvedQuery).matches
  }, [resolvedQuery])

  const getServerSnapshot = useCallback(() => false, [])

  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot)
}
