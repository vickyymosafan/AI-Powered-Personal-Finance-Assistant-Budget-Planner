# 🤖 AI-Powered Personal Finance Assistant & Budget Planner

> **Domain:** Finance & Banking
> **Type:** Capstone Project — Generative AI Application
> **Timeline:** 6 Weeks

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Objectives & Bloom's Taxonomy](#objectives--blooms-taxonomy)
4. [System Architecture](#system-architecture)
5. [Technology Stack](#technology-stack)
6. [Project Structure](#project-structure)
7. [Feature Modules](#feature-modules)
8. [API Endpoints](#api-endpoints)
9. [AI Integration](#ai-integration)
10. [Work Breakdown Structure (WBS)](#work-breakdown-structure-wbs)
11. [Development Timeline](#development-timeline)
12. [Deliverables](#deliverables)
13. [Evaluation Criteria](#evaluation-criteria)
14. [Getting Started](#getting-started)
15. [Environment Variables](#environment-variables)
16. [Development Scripts](#development-scripts)
17. [Current Progress & Status](#current-progress--status)

---

## Executive Summary

Proyek ini mengembangkan **Personal Finance Assistant** berbasis AI yang memanfaatkan kekuatan **Generative AI (Gemini)** untuk membantu pengguna mengelola keuangan secara efektif. Aplikasi menyediakan fitur seperti:

- 📊 **Budget Planning** — Perencanaan anggaran berbasis AI
- 💸 **Expense Analysis** — Analisis pengeluaran dengan breakdown kategori
- 🤖 **AI Financial Advisor** — Chatbot penasihat keuangan
- 🎯 **Savings Goal Planning** — Perencanaan target tabungan
- 📈 **Investment Guidance** — Panduan investasi dasar
- 📄 **Report Generation** — Laporan keuangan visual

Proyek ini menekankan penerapan praktis AI di bidang keuangan, dengan fokus pada **prompt engineering**, **data visualization**, dan **user interface design**.

---

## Problem Statement

Banyak individu kesulitan mengelola keuangan pribadi secara efektif, yang menyebabkan **tekanan finansial** dan **peluang yang terlewatkan**. Hambatan utama:

1. **Kurangnya alat yang mudah diakses** dan user-friendly untuk perencanaan keuangan
2. **Rendahnya literasi finansial** di kalangan masyarakat umum
3. **Tidak adanya personalisasi** dalam saran keuangan yang tersedia
4. **Kompleksitas analisis pengeluaran** tanpa bantuan teknologi

Proyek ini bertujuan mengatasi masalah tersebut dengan mengembangkan asisten keuangan bertenaga AI yang memberikan **saran keuangan personal**, **perencanaan anggaran**, dan **analisis pengeluaran**, memberdayakan pengguna untuk membuat keputusan finansial yang tepat.

---

## Objectives & Bloom's Taxonomy

| # | Objective | Bloom's Level | Deskripsi |
|---|-----------|---------------|-----------|
| 1 | Memahami penerapan Generative AI dalam aplikasi keuangan | **Understand** | Pemahaman konseptual AI di domain finance |
| 2 | Membangun financial tools berbasis AI menggunakan local development | **Apply** | Implementasi praktis dengan VS Code |
| 3 | Mengintegrasikan LLM APIs (Gemini) ke dalam aplikasi | **Apply** | Koneksi dan pemanfaatan API AI |
| 4 | Menerapkan prompt engineering untuk financial insights | **Apply** | Teknik prompt untuk output keuangan berkualitas |
| 5 | Mengembangkan aplikasi tanpa database dependency* | **Apply** | Arsitektur aplikasi mandiri |
| 6 | Membuat dashboard interaktif dengan real-time AI outputs | **Create** | Desain dan implementasi UI |

> *\*Catatan: Implementasi aktual menggunakan PostgreSQL + AsyncPG untuk persistensi data production-grade, melampaui requirement awal.*

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MONOREPO (Turborepo)                  │
│                                                         │
│  ┌──────────────────────┐  ┌──────────────────────────┐ │
│  │    apps/web           │  │      apps/api            │ │
│  │   (Next.js 16)        │  │     (FastAPI)            │ │
│  │                       │  │                          │ │
│  │  ┌─────────────────┐  │  │  ┌────────────────────┐  │ │
│  │  │ App Router       │  │  │  │ Feature Routers    │  │ │
│  │  │ (auth)(dashboard)│  │  │  │ auth, budgets,     │  │ │
│  │  └─────────────────┘  │  │  │ transactions,      │  │ │
│  │  ┌─────────────────┐  │  │  │ analytics, ai      │  │ │
│  │  │ Features         │  │  │  └────────────────────┘  │ │
│  │  │ 6 modules        │  │  │  ┌────────────────────┐  │ │
│  │  └─────────────────┘  │  │  │ Infrastructure     │  │ │
│  │  ┌─────────────────┐  │  │  │ Gemini Client      │  │ │
│  │  │ Core/Shared      │  │  │  └────────────────────┘  │ │
│  │  │ Providers,Config │  │  │  ┌────────────────────┐  │ │
│  │  └─────────────────┘  │  │  │ Core               │  │ │
│  └──────────────────────┘  │  │ Config, DB, Auth    │  │ │
│                            │  └────────────────────┘  │ │
│  ┌──────────────────────┐  └──────────────────────────┘ │
│  │   packages/           │                              │
│  │   ui, eslint-config,  │  ┌──────────────────────────┐│
│  │   typescript-config   │  │   External Services      ││
│  └──────────────────────┘  │   Google Gemini API       ││
│                            │   PostgreSQL (AsyncPG)    ││
│                            └──────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

### Architecture Pattern

- **Frontend**: Feature-Based Architecture (Clean Architecture)
- **Backend**: Clean Architecture with Application Factory Pattern
- **Communication**: REST API (`/api/v1/*`)
- **State Management**: Zustand (client) + React Query (server state)

---

## Technology Stack

### Frontend (`apps/web`)

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 16.2.4 | React framework (App Router) |
| React | 19.2.4 | UI library |
| TypeScript | 5.x | Type safety |
| Tailwind CSS | 4.x | Utility-first CSS |
| shadcn/ui | 4.7.0 | Component library (base-nova style) |
| Zustand | 5.0.13 | Client state management |
| TanStack React Query | 5.100.9 | Server state & caching |
| React Hook Form | 7.75.0 | Form management |
| Zod | 4.4.3 | Schema validation |
| Framer Motion | 12.38.0 | Animations |
| Lucide React | 1.14.0 | Icon library |

### Backend (`apps/api`)

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | ≥3.11 | Runtime |
| FastAPI | ≥0.128.0 | Web framework |
| Uvicorn | ≥0.34.0 | ASGI server |
| SQLAlchemy | ≥2.0.36 | ORM (async) |
| AsyncPG | ≥0.30.0 | PostgreSQL driver |
| Alembic | ≥1.14.0 | Database migrations |
| Pydantic | ≥2.10.0 | Data validation |
| Google GenAI | ≥1.0.0 | Gemini AI SDK |
| python-jose | ≥3.3.0 | JWT tokens |
| Passlib (bcrypt) | ≥1.7.4 | Password hashing |

### Infrastructure

| Technology | Purpose |
|------------|---------|
| Turborepo | Monorepo orchestration |
| pnpm | Package manager (v9) |
| PostgreSQL | Database |
| Prettier | Code formatting |
| Ruff | Python linting |
| ESLint | JS/TS linting |

---

## Project Structure

```
financeai/
├── apps/
│   ├── web/                          # Frontend (Next.js 16)
│   │   ├── src/
│   │   │   ├── app/                  # App Router
│   │   │   │   ├── (auth)/           # Auth route group
│   │   │   │   ├── (dashboard)/      # Dashboard route group
│   │   │   │   ├── globals.css       # Design tokens (oklch)
│   │   │   │   ├── layout.tsx        # Root layout + providers
│   │   │   │   ├── page.tsx          # Landing page
│   │   │   │   ├── error.tsx         # Error boundary
│   │   │   │   └── loading.tsx       # Loading state
│   │   │   ├── features/             # Feature modules
│   │   │   │   ├── ai-assistant/     # AI chatbot UI
│   │   │   │   ├── analytics/        # Charts & insights
│   │   │   │   ├── auth/             # Login/register
│   │   │   │   ├── budgets/          # Budget planner
│   │   │   │   ├── dashboard/        # Main dashboard
│   │   │   │   └── transactions/     # Expense tracking
│   │   │   ├── core/                 # Core infrastructure
│   │   │   │   ├── api/              # API client
│   │   │   │   ├── config/           # App configuration
│   │   │   │   ├── guards/           # Route protection
│   │   │   │   └── providers/        # React providers
│   │   │   ├── components/ui/        # shadcn/ui components
│   │   │   ├── shared/               # Shared utilities
│   │   │   │   ├── components/       # Reusable components
│   │   │   │   ├── constants/        # App constants
│   │   │   │   ├── hooks/            # Custom hooks
│   │   │   │   ├── lib/              # Utility functions
│   │   │   │   └── types/            # TypeScript types
│   │   │   └── lib/utils.ts          # cn() utility
│   │   ├── components.json           # shadcn/ui config
│   │   └── package.json
│   │
│   └── api/                          # Backend (FastAPI)
│       ├── app/
│       │   ├── main.py               # App factory entry point
│       │   ├── core/                 # Core layer
│       │   │   ├── config.py         # Pydantic Settings
│       │   │   ├── database.py       # Async SQLAlchemy engine
│       │   │   ├── security.py       # JWT + bcrypt
│       │   │   ├── middleware.py     # Custom middleware
│       │   │   ├── exceptions.py     # Exception handlers
│       │   │   └── dependencies.py   # DI dependencies
│       │   ├── features/             # Feature modules
│       │   │   ├── auth/router.py
│       │   │   ├── budgets/router.py
│       │   │   ├── transactions/router.py
│       │   │   ├── analytics/router.py
│       │   │   └── ai_assistant/router.py
│       │   ├── infrastructure/       # External services
│       │   │   └── gemini/client.py  # Gemini AI wrapper
│       │   └── shared/               # Shared utilities
│       ├── pyproject.toml
│       └── requirements.txt
│
├── packages/                         # Shared packages
│   ├── ui/                           # Shared UI library
│   ├── eslint-config/                # ESLint configs
│   └── typescript-config/            # TSConfig presets
│
├── turbo.json                        # Turborepo config
├── pnpm-workspace.yaml               # Workspace definition
└── package.json                      # Root scripts
```

---

## Feature Modules

### 1. 🔐 Authentication (`auth`)
- Login & Register dengan JWT
- Access Token + Refresh Token
- Password hashing (bcrypt)
- Route protection (guards)

### 2. 📊 Budget Planner (`budgets`)
- Input pendapatan dan alokasi anggaran
- AI-based budget allocation (Gemini)
- Rekomendasi distribusi anggaran (50/30/20 rule, dll)
- Visual budget breakdown

### 3. 💸 Expense Analyzer (`transactions`)
- Input detail pengeluaran
- Category-wise breakdown otomatis
- Trend analysis per periode
- AI-generated spending insights

### 4. 🤖 AI Financial Advisor (`ai-assistant`)
- Chat interface real-time
- Tanya jawab keuangan dengan Gemini
- Saran personalisasi berdasarkan data pengguna
- Response formatting (markdown, structured data)

### 5. 📈 Analytics & Visualization (`analytics`)
- Dashboard overview keuangan
- Grafik pengeluaran vs pemasukan
- Trend lines & forecasting
- Savings progress tracking

### 6. 🎯 Savings & Investment
- Target tabungan dengan timeline
- Kalkulasi bulanan otomatis
- Panduan investasi dasar dari AI
- Risk assessment sederhana

---

## API Endpoints

| Method | Endpoint | Feature | Description |
|--------|----------|---------|-------------|
| `POST` | `/api/v1/auth/register` | Auth | Register user baru |
| `POST` | `/api/v1/auth/login` | Auth | Login & dapatkan JWT |
| `POST` | `/api/v1/auth/refresh` | Auth | Refresh access token |
| `GET` | `/api/v1/transactions` | Transactions | List semua transaksi |
| `POST` | `/api/v1/transactions` | Transactions | Tambah transaksi |
| `GET` | `/api/v1/budgets` | Budgets | Get budget plan |
| `POST` | `/api/v1/budgets` | Budgets | Create/update budget |
| `POST` | `/api/v1/budgets/ai-allocate` | Budgets | AI budget allocation |
| `GET` | `/api/v1/analytics/summary` | Analytics | Financial summary |
| `GET` | `/api/v1/analytics/trends` | Analytics | Spending trends |
| `POST` | `/api/v1/ai/chat` | AI Assistant | Chat with AI advisor |
| `POST` | `/api/v1/ai/insights` | AI Assistant | Generate insights |
| `GET` | `/health` | System | Health check |

---

## AI Integration

### Gemini Client Architecture

```python
# Infrastructure Layer — Singleton Pattern
class GeminiClient:
    # Text generation (temperature: 0.7)
    async def generate(prompt, system_instruction, temperature)

    # Structured JSON output (temperature: 0.3)
    async def generate_structured(prompt, system_instruction)
```

### Prompt Engineering Areas

| Area | System Instruction Focus |
|------|-------------------------|
| Budget Allocation | Distribusi pendapatan berdasarkan profil keuangan |
| Expense Insights | Pattern recognition & anomaly detection |
| Financial Advice | Personalized recommendations |
| Savings Planning | Goal-based calculation & timeline |
| Investment Guidance | Risk-appropriate suggestions |

### Model Configuration
- **Model**: `gemini-2.5-flash`
- **Creative tasks**: temperature `0.7`
- **Structured output**: temperature `0.3`, mime `application/json`

---

## Work Breakdown Structure (WBS)

### M1. Project Setup and Core Functionality — Week 1
| # | Task | Status |
|---|------|--------|
| 1.1 | Environment Setup (Monorepo, dependencies, configs) | To Do |
| 1.2 | Basic UI Framework (Layout, routing, design system) | To Do |

### M2. Budget Planner Implementation — Week 2
| # | Task | Status |
|---|------|--------|
| 2.1 | Input Handling (Form, validation, state) | To Do |
| 2.2 | AI Integration (Gemini prompt for budget allocation) | To Do |
| 2.3 | Output Display (Budget breakdown UI) | To Do |

### M3. Expense Analyzer Development — Week 3
| # | Task | Status |
|---|------|--------|
| 3.1 | Expense Input (Transaction form, categories) | To Do |
| 3.2 | Category Breakdown (Auto-categorization, grouping) | To Do |
| 3.3 | Insight Generation (AI-powered spending insights) | To Do |

### M4. AI Financial Advisor (Chatbot) — Week 4
| # | Task | Status |
|---|------|--------|
| 4.1 | Chatbot Interface (Chat UI, message history) | To Do |
| 4.2 | LLM Integration (Streaming responses, context) | To Do |
| 4.3 | Response Formatting (Markdown, structured data) | To Do |

### M5. Savings Goal Planner & Investment Guidance — Week 5
| # | Task | Status |
|---|------|--------|
| 5.1 | Savings Goal Input (Target, timeline, priority) | To Do |
| 5.2 | Savings Plan Generation (Monthly calculation, AI plan) | To Do |
| 5.3 | Investment Guidance (Risk profile, AI recommendations) | To Do |

### M6. Visualization and Report Generation — Week 6
| # | Task | Status |
|---|------|--------|
| 6.1 | Data Visualization (Charts, graphs, dashboards) | To Do |
| 6.2 | Report Generation (PDF/export summary) | To Do |
| 6.3 | Final Testing and Refinement (QA, polish, docs) | To Do |

**Total WBS Items: 23** (6 Milestones + 17 Tasks)

---

## Development Timeline

```
Week 1  ████████░░░░░░░░░░░░░░░░  Setup & Core UI
Week 2  ░░░░░░░░████████░░░░░░░░  Budget Planner
Week 3  ░░░░░░░░░░░░░░░░████████  Expense Analyzer
Week 4  ████████░░░░░░░░░░░░░░░░  AI Chatbot
Week 5  ░░░░░░░░████████░░░░░░░░  Savings & Investment
Week 6  ░░░░░░░░░░░░░░░░████████  Visualization & Polish
```

---

## Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Functional Application** | Aplikasi full-stack yang berjalan lengkap dengan semua fitur |
| 2 | **Source Code** | Repository dengan kode terstruktur dan terdokumentasi |
| 3 | **Project Report** | Laporan proyek mencakup analisis, desain, dan hasil |
| 4 | **Demo Presentation** | Presentasi demo aplikasi dan fitur-fitur utama |
| 5 | **User Manual** | Panduan penggunaan aplikasi untuk end-user |

---

## Evaluation Criteria

| Criteria | Weight | Description |
|----------|--------|-------------|
| **Functionality** | 30% | Semua fitur berjalan sesuai spesifikasi |
| **Code Quality** | 20% | Clean code, best practices, proper architecture |
| **AI Integration** | 20% | Kualitas prompt engineering & AI output |
| **User Interface** | 15% | Desain responsif, UX yang baik, visual appeal |
| **Report Quality** | 10% | Kelengkapan dan kejelasan dokumentasi |
| **Presentation** | 5% | Kemampuan demo dan komunikasi teknis |

```
Functionality   ██████████████████████████████  30%
Code Quality    ████████████████████            20%
AI Integration  ████████████████████            20%
User Interface  ███████████████                 15%
Report Quality  ██████████                      10%
Presentation    █████                            5%
```

---

## Getting Started

### Prerequisites
- **Node.js** ≥ 18
- **pnpm** 9.x
- **Python** ≥ 3.11
- **PostgreSQL** (local or remote)
- **Gemini API Key** ([Google AI Studio](https://aistudio.google.com/))

### Installation

```bash
# 1. Clone repository
git clone <repo-url>
cd AI-Powered-Personal-Finance-Assistant-Budget-Planner

# 2. Install frontend dependencies
pnpm install

# 3. Setup backend virtual environment
cd apps/api
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 4. Configure environment variables
cp apps/web/.env.local.example apps/web/.env.local
cp apps/api/.env.example apps/api/.env

# 5. Run development servers
pnpm dev                     # Runs both web & api via Turborepo
```

---

## Environment Variables

### Frontend (`apps/web/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Backend (`apps/api/.env`)
```env
APP_NAME=FinanceAI API
DEBUG=true
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/financeai
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["http://localhost:3000"]
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash
RATE_LIMIT_PER_MINUTE=60
```

---

## Development Scripts

### Root Level (Turborepo)
```bash
pnpm dev          # Run all apps in dev mode
pnpm dev:web      # Run frontend only
pnpm dev:api      # Run backend only
pnpm build        # Build all apps
pnpm lint         # Lint all packages
pnpm format       # Format with Prettier
pnpm check-types  # TypeScript type checking
```

### Backend Direct
```bash
cd apps/api
uvicorn app.main:app --reload --port 8000
```

---

## Current Progress & Status

### ✅ Completed (Scaffold Phase ~15%)
- [x] Monorepo structure (Turborepo + pnpm workspaces)
- [x] Frontend skeleton (Next.js 16, React 19, Tailwind 4, shadcn/ui)
- [x] Backend skeleton (FastAPI, factory pattern)
- [x] Clean Architecture on both frontend & backend
- [x] Gemini AI client (singleton, async, structured output)
- [x] JWT authentication scaffolding (bcrypt + JOSE)
- [x] Async database session management (SQLAlchemy + AsyncPG)
- [x] All 5 feature routers registered
- [x] Design system (oklch color tokens, light/dark mode)
- [x] State management setup (Zustand + React Query)
- [x] Form handling infrastructure (RHF + Zod)
- [x] Animation support (Framer Motion)

### 🔲 To Do
- [ ] Database models (SQLAlchemy ORM models)
- [ ] Alembic migration setup
- [ ] Feature service implementations
- [ ] Dashboard UI components
- [ ] Data visualization (charting library)
- [ ] Budget planner UI & logic
- [ ] Expense analyzer UI & logic
- [ ] AI chatbot interface
- [ ] Savings goal planner
- [ ] Investment guidance module
- [ ] Report generation
- [ ] Unit & integration tests
- [ ] User manual documentation

---

> **Last Updated:** 2026-05-09
> **Maintained by:** Vicky Mosafan
