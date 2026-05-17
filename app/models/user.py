"""
Kullanıcı (Personel) Modeli
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"           # Yönetici
    WAITER = "waiter"         # Garson
    CHEF = "chef"             # Aşçı/Mutfak
    CASHIER = "cashier"       # Kasiyer

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=True)
    full_name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.WAITER, nullable=False)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # İlişki: Bir kullanıcının birden fazla siparişi olabilir
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
