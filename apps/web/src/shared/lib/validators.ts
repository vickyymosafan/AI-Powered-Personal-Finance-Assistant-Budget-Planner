import { z } from 'zod'

/**
 * Shared Zod primitives
 * Reusable building blocks — compose into feature schemas
 */

export const zRequired = z.string().min(1, 'Field ini wajib diisi')

export const zEmail = z
  .string()
  .min(1, 'Email wajib diisi')
  .email('Format email tidak valid')

export const zPassword = z
  .string()
  .min(8, 'Password minimal 8 karakter')
  .max(100, 'Password maksimal 100 karakter')

export const zPasswordConfirm = (refField: string) =>
  z.string().min(1, 'Konfirmasi password wajib diisi').refine(
    (val) => val === refField,
    { message: 'Password tidak cocok' }
  )

export const zPositiveNumber = z
  .number({ invalid_type_error: 'Harus berupa angka' })
  .positive('Harus lebih dari 0')

export const zCurrencyAmount = z
  .number({ invalid_type_error: 'Harus berupa angka' })
  .min(0, 'Jumlah tidak boleh negatif')
  .max(999_999_999_999, 'Jumlah terlalu besar')

export const zOptionalString = z.string().optional().or(z.literal(''))

export const zIsoDate = z.string().regex(
  /^\d{4}-\d{2}-\d{2}$/,
  'Format tanggal harus YYYY-MM-DD'
)

export const zPaginationParams = z.object({
  page: z.number().int().positive().optional().default(1),
  per_page: z.number().int().positive().max(100).optional().default(20),
  sort_by: z.string().optional(),
  sort_order: z.enum(['asc', 'desc']).optional().default('desc'),
})
