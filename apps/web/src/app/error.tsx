'use client'

import { useEffect } from 'react'

interface GlobalErrorProps {
  error: Error & { digest?: string }
  reset: () => void
}

export default function GlobalError({ error, reset }: GlobalErrorProps) {
  useEffect(() => {
    // Log to monitoring service (e.g. Sentry)
    console.error('[GlobalError]', error)
  }, [error])

  return (
    <html lang="id">
      <body className="flex min-h-screen items-center justify-center bg-background font-sans antialiased">
        <div className="mx-auto max-w-md space-y-6 text-center">
          <div className="space-y-2">
            <h1 className="text-2xl font-bold text-foreground">
              Something went wrong
            </h1>
            <p className="text-sm text-muted-foreground">
              {error.message || 'An unexpected error occurred. Please try again.'}
            </p>
            {error.digest && (
              <p className="text-xs text-muted-foreground/60">
                Error ID: {error.digest}
              </p>
            )}
          </div>

          <div className="flex flex-col gap-2 sm:flex-row sm:justify-center">
            <button
              onClick={reset}
              className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
            >
              Try again
            </button>
            <a
              href="/"
              className="rounded-md border border-border px-4 py-2 text-sm font-medium text-foreground hover:bg-muted"
            >
              Go home
            </a>
          </div>
        </div>
      </body>
    </html>
  )
}
