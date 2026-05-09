import type { Metadata } from 'next'
import { RegisterForm } from '@/features/auth/components/RegisterForm'

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
      <RegisterForm />
    </div>
  )
}
