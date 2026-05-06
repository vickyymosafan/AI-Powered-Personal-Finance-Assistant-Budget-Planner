export const APP_CONSTANTS = {
  // Pagination defaults
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,

  // Debounce
  SEARCH_DEBOUNCE_MS: 300,

  // Cache
  STALE_TIME_MS: 5 * 60 * 1000, // 5 minutes
  GC_TIME_MS: 30 * 60 * 1000, // 30 minutes

  // Date formats
  DATE_FORMAT: 'yyyy-MM-dd',
  DATETIME_FORMAT: 'yyyy-MM-dd HH:mm:ss',

  // Currency
  DEFAULT_CURRENCY: 'IDR' as const,
} as const
