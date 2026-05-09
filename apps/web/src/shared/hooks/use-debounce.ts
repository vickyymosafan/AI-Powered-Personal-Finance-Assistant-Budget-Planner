'use client'

import { useEffect, useState } from 'react'

/**
 * Debounce a rapidly changing value
 * @param value - The value to debounce
 * @param delay - Delay in ms (default: 300)
 */
export function useDebounce<T>(value: T, delay = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])

  return debouncedValue
}
