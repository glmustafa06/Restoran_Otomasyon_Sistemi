"""
Sipariş Detayları Modeli
"""
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class ItemStatus(str, enum.Enum):
    PENDING = "pending"       # Bekliyor
    PREPARING = "preparing"   # Hazırlanıyor
    READY = "ready"           # Hazır
    SERVED = "served"         # Servis edildi
    CANCELLED = "cancelled"  # İptal

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)  # Sipariş anındaki fiyat
    total_price = Column(Float, nullable=False)
    notes = Column(String(300), nullable=True)  # Özel istekler
    status = Column(Enum(ItemStatus), default=ItemStatus.PENDING)

    # İlişkiler
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<OrderItem {self.product_id} x{self.quantity}>"
