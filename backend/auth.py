from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import TokenData, User
from config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()

# In-memory user storage (replace with database in production)
users_db = {}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    # Apply same truncation as when hashing
    plain_password = truncate_password(plain_password, 72)
    return pwd_context.verify(plain_password, hashed_password)


def truncate_password(password: str, max_bytes: int = 72) -> str:
    """
    Truncate password to fit within max_bytes when encoded as UTF-8.
    Ensures we don't cut in the middle of a multi-byte character.
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) <= max_bytes:
        return password
    
    # Truncate and decode, removing any incomplete multi-byte sequences
    truncated = password_bytes[:max_bytes].decode('utf-8', errors='ignore')
    return truncated


def get_password_hash(password: str) -> str:
    """Hash a password."""
    # Bcrypt has a 72 byte limit
    password = truncate_password(password, 72)
    print(f"DEBUG: Password length: {len(password)} chars, {len(password.encode('utf-8'))} bytes")
    print(f"DEBUG: Password: {password[:20]}..." if len(password) > 20 else f"DEBUG: Password: {password}")
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """Decode and verify a JWT access token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(email=email)
    except JWTError:
        raise credentials_exception


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get the current authenticated user."""
    token = credentials.credentials
    token_data = decode_access_token(token)
    
    user_data = users_db.get(token_data.email)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Return User without hashed_password
    return User(
        id=user_data["id"],
        email=user_data["email"],
        full_name=user_data.get("full_name"),
        created_at=user_data["created_at"],
        is_active=user_data["is_active"]
    )


def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate a user with email and password."""
    user_data = users_db.get(email)
    if not user_data:
        return None
    if not verify_password(password, user_data["hashed_password"]):
        return None
    
    # Return User without hashed_password
    return User(
        id=user_data["id"],
        email=user_data["email"],
        full_name=user_data.get("full_name"),
        created_at=user_data["created_at"],
        is_active=user_data["is_active"]
    )


def create_user(email: str, password: str, full_name: Optional[str] = None) -> User:
    """Create a new user."""
    if email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(password)
    created_at = datetime.utcnow()
    user_data = {
        "id": email,  # Simple ID strategy for demo
        "email": email,
        "full_name": full_name,
        "hashed_password": hashed_password,
        "created_at": created_at,
        "is_active": True
    }
    users_db[email] = user_data
    
    # Return User without hashed_password
    return User(
        id=email,
        email=email,
        full_name=full_name,
        created_at=created_at,
        is_active=True
    )
