import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Create Account',
  description: 'Create a new FinanceAI account',
}

export default function RegisterPage() {
  return (
    <div className="space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold tracking-tight">Create an account</h1>
        <p className="text-sm text-muted-foreground">
          Start managing your finances with AI
        </p>
      </div>
      {/* RegisterForm will be implemented in features/auth */}
      <p className="text-center text-xs text-muted-foreground">
        Register form coming soon
      </p>
    </div>
  )
}
