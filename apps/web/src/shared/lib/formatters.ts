/**
 * Shared formatters
 * Pure functions — no side effects, no imports from other layers
 */

const IDR = new Intl.NumberFormat('id-ID', {
  style: 'currency',
  currency: 'IDR',
  minimumFractionDigits: 0,
  maximumFractionDigits: 0,
})

const SHORT_IDR = new Intl.NumberFormat('id-ID', {
  style: 'currency',
  currency: 'IDR',
  notation: 'compact',
  minimumFractionDigits: 0,
  maximumFractionDigits: 1,
})

const DATE_FORMAT = new Intl.DateTimeFormat('id-ID', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
})

const DATETIME_FORMAT = new Intl.DateTimeFormat('id-ID', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
})

const PERCENT_FORMAT = new Intl.NumberFormat('id-ID', {
  style: 'percent',
  minimumFractionDigits: 0,
  maximumFractionDigits: 1,
})

/** Format number as IDR currency: Rp 1.500.000 */
export function formatCurrency(amount: number): string {
  return IDR.format(amount)
}

/** Format number as compact IDR: Rp 1,5 jt */
export function formatCurrencyShort(amount: number): string {
  return SHORT_IDR.format(amount)
}

/** Format date: 07 Mei 2026 */
export function formatDate(date: Date | string): string {
  return DATE_FORMAT.format(new Date(date))
}

/** Format datetime: 07 Mei 2026, 08.00 */
export function formatDateTime(date: Date | string): string {
  return DATETIME_FORMAT.format(new Date(date))
}

/** Format as percentage: 75,5% */
export function formatPercent(value: number): string {
  return PERCENT_FORMAT.format(value)
}

/** Format relative time: "2 jam lalu", "kemarin" */
export function formatRelativeTime(date: Date | string): string {
  const now = new Date()
  const then = new Date(date)
  const diffMs = now.getTime() - then.getTime()
  const diffSec = Math.floor(diffMs / 1000)
  const diffMin = Math.floor(diffSec / 60)
  const diffHour = Math.floor(diffMin / 60)
  const diffDay = Math.floor(diffHour / 24)

  const rtf = new Intl.RelativeTimeFormat('id-ID', { numeric: 'auto' })

  if (diffSec < 60) return rtf.format(-diffSec, 'second')
  if (diffMin < 60) return rtf.format(-diffMin, 'minute')
  if (diffHour < 24) return rtf.format(-diffHour, 'hour')
  if (diffDay < 7) return rtf.format(-diffDay, 'day')
  return formatDate(then)
}

/** Truncate string with ellipsis */
export function truncate(str: string, length: number): string {
  if (str.length <= length) return str
  return `${str.slice(0, length)}...`
}

/** Format file size: 1.2 MB */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`
}
