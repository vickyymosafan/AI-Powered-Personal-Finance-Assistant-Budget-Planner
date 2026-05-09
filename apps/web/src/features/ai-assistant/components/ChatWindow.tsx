'use client'

import { useState } from 'react'
import { useChat } from '../hooks/use-chat'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Bot, Send, User } from 'lucide-react'
import { cn } from '@/lib/utils'

export function ChatWindow() {
  const { messages, sendMessage, isPending } = useChat()
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (!input.trim()) return
    sendMessage(input)
    setInput('')
  }

  return (
    <Card className="w-full h-[600px] flex flex-col glassmorphism">
      <CardHeader className="border-b border-border">
        <CardTitle className="flex items-center gap-2">
          <Bot className="h-5 w-5 text-primary" />
          AI Financial Advisor
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-muted-foreground mt-20">
            <Bot className="h-12 w-12 mx-auto mb-4 text-muted-foreground/50" />
            <p>Halo! Saya adalah asisten keuangan AI Anda.</p>
            <p className="text-sm">Tanyakan tentang anggaran, tren pengeluaran, atau saran investasi.</p>
          </div>
        )}
        
        {messages.map((message) => {
          const isAssistant = message.role === 'assistant'
          return (
            <div
              key={message.id}
              className={cn(
                'flex items-start gap-3',
                isAssistant ? 'justify-start' : 'justify-end'
              )}
            >
              {isAssistant && (
                <Avatar className="h-8 w-8">
                  <AvatarFallback className="bg-primary text-primary-foreground">
                    <Bot className="h-4 w-4" />
                  </AvatarFallback>
                </Avatar>
              )}
              <div
                className={cn(
                  'max-w-[70%] rounded-lg px-3 py-2 text-sm',
                  isAssistant
                    ? 'bg-muted text-muted-foreground'
                    : 'bg-primary text-primary-foreground'
                )}
              >
                {message.content}
              </div>
              {!isAssistant && (
                <Avatar className="h-8 w-8">
                  <AvatarFallback>
                    <User className="h-4 w-4" />
                  </AvatarFallback>
                </Avatar>
              )}
            </div>
          )
        })}
        
        {isPending && (
          <div className="flex items-start gap-3 justify-start">
            <Avatar className="h-8 w-8">
              <AvatarFallback className="bg-primary text-primary-foreground">
                <Bot className="h-4 w-4" />
              </AvatarFallback>
            </Avatar>
            <div className="bg-muted text-muted-foreground max-w-[70%] rounded-lg px-3 py-2 text-sm">
              <span className="animate-pulse">Mengetik...</span>
            </div>
          </div>
        )}
      </CardContent>
      <CardFooter className="border-t border-border p-4">
        <form
          onSubmit={(e) => {
            e.preventDefault()
            handleSend()
          }}
          className="flex w-full items-center gap-2"
        >
          <Input
            placeholder="Ketik pesan Anda..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isPending}
            className="flex-1"
          />
          <Button type="submit" size="icon" disabled={isPending || !input.trim()}>
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </CardFooter>
    </Card>
  )
}
