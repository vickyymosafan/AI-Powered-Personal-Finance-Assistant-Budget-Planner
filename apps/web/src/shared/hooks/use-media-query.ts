'use client'

import { useEffect, useState } from 'react'

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

  const [matches, setMatches] = useState(false)

  useEffect(() => {
    if (typeof window === 'undefined') return
    const media = window.matchMedia(resolvedQuery)
    setMatches(media.matches)

    const handler = (e: MediaQueryListEvent) => setMatches(e.matches)
    media.addEventListener('change', handler)
    return () => media.removeEventListener('change', handler)
  }, [resolvedQuery])

  return matches
}
