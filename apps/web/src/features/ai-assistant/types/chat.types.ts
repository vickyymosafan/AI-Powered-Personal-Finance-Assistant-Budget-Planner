export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface ChatRequest {
  message: string
  history?: Message[]
}

export interface ChatResponse {
  response: string
}
