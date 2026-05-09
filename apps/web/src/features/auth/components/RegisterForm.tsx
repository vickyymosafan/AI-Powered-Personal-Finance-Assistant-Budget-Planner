'use client'

import Link from 'next/link'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { registerSchema, type RegisterFormValues } from '../schemas/auth.schema'
import { useRegister } from '../hooks/use-register'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { AlertCircle } from 'lucide-react'

export function RegisterForm() {
  const { mutate: registerUser, isPending, error } = useRegister()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      full_name: '',
      email: '',
      password: '',
      confirm_password: '',
    },
  })

  function onSubmit(data: RegisterFormValues) {
    registerUser({
      full_name: data.full_name,
      email: data.email,
      password: data.password,
    })
  }

  return (
    <div className="grid gap-6">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              {error.message || 'Gagal mendaftar, silakan coba lagi.'}
            </AlertDescription>
          </Alert>
        )}

        <div className="space-y-2">
          <Label htmlFor="full_name">Nama Lengkap</Label>
          <Input
            id="full_name"
            placeholder="John Doe"
            {...register('full_name')}
          />
          {errors.full_name && (
            <p className="text-[0.8rem] font-medium text-destructive">
              {errors.full_name.message}
            </p>
          )}
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            placeholder="johndoe@example.com"
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

        <div className="space-y-2">
          <Label htmlFor="confirm_password">Konfirmasi Password</Label>
          <Input
            id="confirm_password"
            placeholder="••••••••"
            type="password"
            {...register('confirm_password')}
          />
          {errors.confirm_password && (
            <p className="text-[0.8rem] font-medium text-destructive">
              {errors.confirm_password.message}
            </p>
          )}
        </div>

        <Button type="submit" className="w-full" disabled={isPending}>
          {isPending ? 'Mendaftar...' : 'Daftar'}
        </Button>
        <div className="text-center text-sm text-muted-foreground">
          Sudah punya akun?{' '}
          <Link href="/login" className="text-primary hover:underline">
            Sign In
          </Link>
        </div>
      </form>
    </div>
  )
}
