import pytest
from app.core.security import get_password_hash, verify_password, create_access_token, verify_token
from app.domain.auth.service import create_user, authenticate_user
from app.schemas.auth import UserCreate
from app.core.exceptions import AuthenticationError


@pytest.mark.asyncio
async def test_password_hashing():
    raw_password = "SecretPassword123!"
    hashed = get_password_hash(raw_password)
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


@pytest.mark.asyncio
async def test_jwt_token_generation_and_decoding():
    token = create_access_token(subject=101, role="DATA_ENGINEER")
    assert isinstance(token, str)
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "101"
    assert payload["role"] == "DATA_ENGINEER"


@pytest.mark.asyncio
async def test_user_creation_and_authentication(db_session):
    user_in = UserCreate(
        email="engineer@dataforge.io",
        password="SecureDevPassword2026",
        full_name="Jane Data Engineer",
        role_id=3  # Data Engineer
    )
    created_user = await create_user(db_session, user_in)
    assert created_user.id is not None
    assert created_user.email == "engineer@dataforge.io"

    # Test valid login
    authed_user = await authenticate_user(db_session, "engineer@dataforge.io", "SecureDevPassword2026")
    assert authed_user.id == created_user.id

    # Test invalid password login
    with pytest.raises(AuthenticationError):
        await authenticate_user(db_session, "engineer@dataforge.io", "InvalidPass")
