"""
Auth feature — Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field


# ── Request Schemas ──────────────────────────────────────────────


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=100)
    currency: str = Field(default="IDR", min_length=3, max_length=3)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UpdateProfileRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    monthly_income: float | None = Field(default=None, ge=0)


# ── Response Schemas ─────────────────────────────────────────────


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool
    currency: str
    monthly_income: float | None
    created_at: str

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    user: UserResponse
    tokens: TokenResponse
