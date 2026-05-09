import { z } from 'zod'
import { zCurrencyAmount, zIsoDate, zOptionalString } from '@/shared/lib/validators'
import { TRANSACTION_CATEGORIES, TRANSACTION_TYPES } from '@/shared/constants/app.constants'

export const transactionSchema = z.object({
  type: z.enum(TRANSACTION_TYPES, 'Tipe transaksi wajib dipilih'),
  category: z.enum(TRANSACTION_CATEGORIES, 'Kategori wajib dipilih'),
  amount: zCurrencyAmount,
  description: z.string().min(1, 'Deskripsi wajib diisi').max(255),
  date: zIsoDate,
  notes: zOptionalString,
})

export type TransactionFormValues = z.infer<typeof transactionSchema>
