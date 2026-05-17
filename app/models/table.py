"""
Masa Modeli
"""
from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TableStatus(str, enum.Enum):
    EMPTY = "empty"           # Boş
    OCCUPIED = "occupied"     # Dolu/Sipariş alındı
    RESERVED = "reserved"     # Rezerve
    CLEANING = "cleaning"     # Temizleniyor

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String(10), unique=True, nullable=False)
    section = Column(String(50), default="İç Mekan")  # İç Mekan, Bahçe, Üst Kat
    capacity = Column(Integer, default=4)
    status = Column(Enum(TableStatus), default=TableStatus.EMPTY)
    position_x = Column(Float, default=0.0)  # Görsel konum
    position_y = Column(Float, default=0.0)

    # İlişki: Bir masanın birden fazla siparişi olabilir
    orders = relationship("Order", back_populates="table")

    def __repr__(self):
        return f"<Table {self.table_number} ({self.status})>"
