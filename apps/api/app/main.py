"""
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.middleware import register_middleware

# Eagerly import ALL ORM models so SQLAlchemy mapper resolves relationships correctly.
# Without this, string references like "Transaction" may resolve to sqlalchemy internals.
import app.features.auth.models  # noqa: F401
import app.features.transactions.models  # noqa: F401
import app.features.budgets.models  # noqa: F401
import app.features.analytics.models  # noqa: F401

from app.features.auth.router import router as auth_router
from app.features.transactions.router import router as transactions_router
from app.features.budgets.router import router as budgets_router
from app.features.analytics.router import router as analytics_router
from app.features.ai_assistant.router import router as ai_router


def create_app() -> FastAPI:
    """Application factory pattern"""
    app = FastAPI(
        title=settings.APP_NAME,
        description="AI-Powered Personal Finance Assistant & Budget Planner API",
        version="0.1.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom middleware
    register_middleware(app)

    # Feature routers
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(transactions_router, prefix="/api/v1/transactions", tags=["transactions"])
    app.include_router(budgets_router, prefix="/api/v1/budgets", tags=["budgets"])
    app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["analytics"])
    app.include_router(ai_router, prefix="/api/v1/ai", tags=["ai-assistant"])

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "healthy", "version": "0.1.0"}

    return app


app = create_app()
