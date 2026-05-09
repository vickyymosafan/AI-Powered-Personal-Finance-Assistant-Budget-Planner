import type { Metadata } from 'next'
import { ChatWindow } from '@/features/ai-assistant/components/ChatWindow'

export const metadata: Metadata = {
  title: 'AI Assistant',
  description: 'Your personal AI-powered financial advisor',
}

export default function AiAssistantPage() {
  return (
    <div className="flex h-full flex-col space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">AI Assistant</h1>
        <p className="text-sm text-muted-foreground">
          Ask anything about your finances
        </p>
      </div>
      <ChatWindow />
    </div>
  )
}
