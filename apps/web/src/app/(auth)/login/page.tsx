import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Sign In',
  description: 'Sign in to your FinanceAI account',
}

export default function LoginPage() {
  return (
    <div className="space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold tracking-tight">Welcome back</h1>
        <p className="text-sm text-muted-foreground">
          Sign in to your FinanceAI account
        </p>
      </div>
      {/* LoginForm will be implemented in features/auth */}
      <p className="text-center text-xs text-muted-foreground">
        Login form coming soon
      </p>
    </div>
  )
}
