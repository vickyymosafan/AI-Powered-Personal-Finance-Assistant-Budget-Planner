'use client'

import Link from 'next/link'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { loginSchema, type LoginFormValues } from '../schemas/auth.schema'
import { useLogin } from '../hooks/use-login'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { AlertCircle } from 'lucide-react'

export function LoginForm() {
  const { mutate: login, isPending, error } = useLogin()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  })

  function onSubmit(data: LoginFormValues) {
    login(data)
  }

  return (
    <div className="grid gap-6">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              {error.message || 'Login gagal, periksa email dan password Anda.'}
            </AlertDescription>
          </Alert>
        )}
        
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            placeholder="vicky@financeai.com"
            type="email"
            {...register('email')}
          />
          {errors.email && (
            <p className="text-[0.8rem] font-medium text-destructive">
              {errors.email.message}
            </p>
          )}
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            placeholder="••••••••"
            type="password"
            {...register('password')}
          />
          {errors.password && (
            <p className="text-[0.8rem] font-medium text-destructive">
              {errors.password.message}
            </p>
          )}
        </div>

        <Button type="submit" className="w-full" disabled={isPending}>
          {isPending ? 'Signing in...' : 'Sign In'}
        </Button>
        <div className="text-center text-sm text-muted-foreground">
          Belum punya akun?{' '}
          <Link href="/register" className="text-primary hover:underline">
            Daftar
          </Link>
        </div>
      </form>
    </div>
  )
}
