'use client'

import * as React from 'react'
import {
  useFormContext,
  type FieldValues,
  type Path,
  type RegisterOptions,
} from 'react-hook-form'
import { cn } from '@/lib/utils'

interface FormFieldProps<T extends FieldValues> {
  name: Path<T>
  label?: string
  description?: string
  required?: boolean
  rules?: RegisterOptions<T>
  className?: string
  children: (props: {
    id: string
    name: Path<T>
    'aria-describedby': string | undefined
    'aria-invalid': boolean
  }) => React.ReactNode
}

/**
 * Context-aware form field wrapper
 * Connects React Hook Form state to any input component
 * Handles: label, error message, description, aria attributes
 */
export function FormField<T extends FieldValues>({
  name,
  label,
  description,
  required,
  className,
  children,
}: FormFieldProps<T>) {
  const {
    formState: { errors },
  } = useFormContext<T>()

  const id = `field-${name}`
  const descriptionId = description ? `${id}-description` : undefined
  const errorId = `${id}-error`

  const error = errors[name]
  const errorMessage = error?.message as string | undefined

  return (
    <div className={cn('space-y-1.5', className)}>
      {label && (
        <label
          htmlFor={id}
          className="text-sm font-medium leading-none text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
        >
          {label}
          {required && (
            <span className="ml-0.5 text-destructive" aria-hidden="true">
              *
            </span>
          )}
        </label>
      )}

      {children({
        id,
        name,
        'aria-describedby': errorMessage ? errorId : descriptionId,
        'aria-invalid': !!errorMessage,
      })}

      {description && !errorMessage && (
        <p id={descriptionId} className="text-xs text-muted-foreground">
          {description}
        </p>
      )}

      {errorMessage && (
        <p id={errorId} role="alert" className="text-xs text-destructive">
          {errorMessage}
        </p>
      )}
    </div>
  )
}
