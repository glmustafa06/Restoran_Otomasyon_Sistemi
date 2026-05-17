"""
Sipariş Modeli
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class OrderStatus(str, enum.Enum):
    PENDING = "pending"       # Bekliyor
    PREPARING = "preparing"   # Hazırlanıyor
    READY = "ready"           # Hazır
    SERVED = "served"         # Servis edildi
    PAID = "paid"             # Ödendi
    CANCELLED = "cancelled"  # İptal

class PaymentStatus(str, enum.Enum):
    UNPAID = "unpaid"         # Ödenmedi
    PARTIAL = "partial"       # Kısmen ödendi
    PAID = "paid"             # Tamamen ödendi

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Siparişi alan personel
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.UNPAID)
    total_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    final_amount = Column(Float, default=0.0)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)

    # İlişkiler
    table = relationship("Table", back_populates="orders")
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order")

    def __repr__(self):
        return f"<Order #{self.id} - Table {self.table_id} ({self.status})>"
