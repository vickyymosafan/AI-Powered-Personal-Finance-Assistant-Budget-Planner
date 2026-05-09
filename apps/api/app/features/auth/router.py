"""
Auth feature — API Router
Full implementation: register, login, refresh, me, update profile
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.features.auth.schemas import (
    AuthResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UpdateProfileRequest,
    UserResponse,
)
from app.features.auth.service import AuthService

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Register akun baru dan dapatkan token."""
    return await AuthService.register(db, payload)


@router.post("/login", response_model=AuthResponse)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Login dengan email dan password."""
    return await AuthService.login(db, payload)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(payload: RefreshRequest):
    """Dapatkan token baru dari refresh token."""
    return await AuthService.refresh(payload.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Dapatkan profil user yang sedang login."""
    return await AuthService.get_me(db, user_id)


@router.patch("/me", response_model=UserResponse)
async def update_profile(
    payload: UpdateProfileRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update profil user (full_name, currency, monthly_income)."""
    return await AuthService.update_profile(db, user_id, payload)
