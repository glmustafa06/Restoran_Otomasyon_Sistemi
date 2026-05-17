"""
Ödeme Modeli
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class PaymentMethod(str, enum.Enum):
    CASH = "cash"             # Nakit
    CREDIT_CARD = "credit_card"  # Kredi Kartı
    DEBIT_CARD = "debit_card"    # Banka Kartı
    MOBILE = "mobile"         # Mobil Ödeme
    MEAL_CARD = "meal_card"   # Yemek Kartı

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    tip = Column(Float, default=0.0)  # Bahşiş
    receipt_number = Column(String(50), nullable=True)
    notes = Column(String(300), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # İlişki
    order = relationship("Order", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.amount}₺ ({self.payment_method})>"
