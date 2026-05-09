'use client'

import { useMutation } from '@tanstack/react-query'
import { apiClient } from '@/core/api/client'
import { API_ENDPOINTS } from '@/core/api/endpoints'
import { useState } from 'react'
import type { Message, ChatRequest, ChatResponse } from '../types/chat.types'

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])

  const mutation = useMutation({
    mutationFn: (data: ChatRequest) =>
      apiClient.post<ChatResponse>(API_ENDPOINTS.AI.CHAT, data),
    
    onSuccess: (data, variables) => {
      // Add user message and assistant response to history
      const userMessage: Message = {
        id: crypto.randomUUID(),
        role: 'user',
        content: variables.message,
        created_at: new Date().toISOString(),
      }

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: data.response,
        created_at: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, userMessage, assistantMessage])
    },
  })

  const sendMessage = (message: string) => {
    mutation.mutate({ message, history: messages })
  }

  return {
    messages,
    sendMessage,
    isPending: mutation.isPending,
    error: mutation.error,
  }
}
