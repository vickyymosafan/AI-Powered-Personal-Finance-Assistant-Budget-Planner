import { env } from './env'

export const siteConfig = {
  name: env.NEXT_PUBLIC_APP_NAME,
  description: 'AI-Powered Personal Finance Assistant & Budget Planner',
  url: env.NEXT_PUBLIC_APP_URL,
  ogImage: `${env.NEXT_PUBLIC_APP_URL}/og.png`,
  links: {
    github: '#',
  },
  creator: 'FinanceAI Team',
} as const

export type SiteConfig = typeof siteConfig
