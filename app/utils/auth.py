from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
from app.models.user import TokenData, UserType
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def _truncate_password(password: str) -> bytes:
    """
    Truncate password to 72 bytes for bcrypt compatibility.
    Uses SHA256 hash for long passwords to maintain security.
    """
    password_bytes = password.encode('utf-8')
    
    # If password is longer than 72 bytes, hash it first
    if len(password_bytes) > 72:
        # Use SHA256 to create a fixed-length hash
        return hashlib.sha256(password_bytes).hexdigest().encode('utf-8')
    
    return password_bytes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        # Truncate password if needed
        password_to_verify = _truncate_password(plain_password).decode('utf-8')
        return pwd_context.verify(password_to_verify, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hash a password"""
    try:
        # Truncate password if needed
        password_to_hash = _truncate_password(password).decode('utf-8')
        return pwd_context.hash(password_to_hash)
    except Exception as e:
        print(f"Password hashing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error hashing password"
        )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """Decode JWT access token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        user_type: str = payload.get("user_type")
        
        if email is None:
            raise credentials_exception
            
        token_data = TokenData(email=email, user_type=user_type)
        return token_data
        
    except JWTError:
        raise credentials_exception


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Get current authenticated user from token"""
    token = credentials.credentials
    return decode_access_token(token)


async def get_current_recruiter(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """Verify current user is a recruiter"""
    if current_user.user_type not in [UserType.RECRUITER.value, UserType.ADMIN.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Recruiter access required."
        )
    return current_user


async def get_current_candidate(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """Verify current user is a candidate"""
    if current_user.user_type != UserType.CANDIDATE.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Candidate access required."
        )
    return current_user
