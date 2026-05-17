"""
Kimlik Doğrulama Servisi
"""
from sqlalchemy.orm import Session
from app.models import User
from app.utils.security import verify_password

def authenticate_user(db: Session, username: str, password: str):
    """Kullanıcı adı ve şifre ile giriş yapar"""
    # Trim whitespace
    username = username.strip() if username else ""
    password = password.strip() if password else ""
    
    # Kullanıcıyı bul
    user = db.query(User).filter(User.username == username, User.is_active == True).first()
    if not user:
        print(f"[AUTH] User not found: {username}")
        return None
    
    # Şifre kontrolü
    if not verify_password(password, user.password_hash):
        print(f"[AUTH] Invalid password for user: {username}")
        return None
    
    print(f"[AUTH] Success: {username} (Role: {user.role})")
    return user
