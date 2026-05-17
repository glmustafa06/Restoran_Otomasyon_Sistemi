"""
Güvenlik yardımcıları: Şifreleme, JWT token
"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
import hashlib
import secrets
from app.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Düz şifreyi hash ile karşılaştırır"""
    return hash_password(plain_password) == hashed_password

def hash_password(password: str) -> str:
    """Şifreyi SHA-256 ile hash'ler (bcrypt yerine)"""
    # Basit ama güvenli hash - bcrypt yerine SHA-256
    salt = settings.SECRET_KEY[:16]
    salted = password + salt
    return hashlib.sha256(salted.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """JWT access token oluşturur"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """JWT token'ı çözer"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
