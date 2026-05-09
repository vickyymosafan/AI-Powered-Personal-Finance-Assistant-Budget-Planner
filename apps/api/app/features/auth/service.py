"""
Auth feature — Business logic service
Handles user registration, authentication, and token management.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError, NotFoundError, UnauthorizedError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.features.auth.models import User
from app.features.auth.schemas import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UpdateProfileRequest,
    UserResponse,
)


def _build_user_response(user: User) -> UserResponse:
    """Convert User ORM model to UserResponse schema."""
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        currency=user.currency,
        monthly_income=user.monthly_income,
        created_at=user.created_at.isoformat(),
    )


def _build_tokens(user_id: str) -> TokenResponse:
    """Generate access + refresh token pair."""
    return TokenResponse(
        access_token=create_access_token(data={"sub": user_id}),
        refresh_token=create_refresh_token(data={"sub": user_id}),
    )


class AuthService:
    """Stateless auth service — receives db session per call."""

    @staticmethod
    async def register(db: AsyncSession, payload: RegisterRequest) -> AuthResponse:
        """Register a new user account."""
        # Check duplicate email
        stmt = select(User).where(User.email == payload.email)
        result = await db.execute(stmt)
        if result.scalar_one_or_none() is not None:
            raise ConflictError(detail="Email sudah terdaftar")

        # Create user
        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name,
            currency=payload.currency.upper(),
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)

        return AuthResponse(
            user=_build_user_response(user),
            tokens=_build_tokens(user.id),
        )

    @staticmethod
    async def login(db: AsyncSession, payload: LoginRequest) -> AuthResponse:
        """Authenticate user with email + password."""
        stmt = select(User).where(User.email == payload.email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None or not verify_password(payload.password, user.hashed_password):
            raise UnauthorizedError(detail="Email atau password salah")

        if not user.is_active:
            raise UnauthorizedError(detail="Akun dinonaktifkan")

        return AuthResponse(
            user=_build_user_response(user),
            tokens=_build_tokens(user.id),
        )

    @staticmethod
    async def refresh(refresh_token: str) -> TokenResponse:
        """Issue new token pair from a valid refresh token."""
        payload = decode_token(refresh_token)
        if payload is None:
            raise UnauthorizedError(detail="Refresh token tidak valid atau kedaluwarsa")

        token_type = payload.get("type")
        if token_type != "refresh":
            raise BadRequestError(detail="Token bukan refresh token")

        user_id = payload.get("sub")
        if user_id is None:
            raise UnauthorizedError(detail="Token payload tidak valid")

        return _build_tokens(user_id)

    @staticmethod
    async def get_me(db: AsyncSession, user_id: str) -> UserResponse:
        """Get current authenticated user profile."""
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise NotFoundError(detail="User tidak ditemukan")

        return _build_user_response(user)

    @staticmethod
    async def update_profile(
        db: AsyncSession, user_id: str, payload: UpdateProfileRequest
    ) -> UserResponse:
        """Update current user profile fields."""
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise NotFoundError(detail="User tidak ditemukan")

        # Only update fields that are explicitly provided
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await db.flush()
        await db.refresh(user)

        return _build_user_response(user)
