import { z } from 'zod'
import { zEmail, zPassword } from '@/shared/lib/validators'

/** Login form schema */
export const loginSchema = z.object({
  email: zEmail,
  password: z.string().min(1, 'Password wajib diisi'),
})

/** Register form schema */
export const registerSchema = z
  .object({
    full_name: z.string().min(2, 'Nama minimal 2 karakter').max(100),
    email: zEmail,
    password: zPassword,
    confirm_password: z.string().min(1, 'Konfirmasi password wajib diisi'),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: 'Password tidak cocok',
    path: ['confirm_password'],
  })

export type LoginFormValues = z.infer<typeof loginSchema>
export type RegisterFormValues = z.infer<typeof registerSchema>
