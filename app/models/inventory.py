"""
Stok / Envanter Modeli
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String(150), nullable=False)
    unit = Column(String(20), nullable=False)  # kg, adet, litre, vs.
    quantity = Column(Float, default=0.0)
    min_stock = Column(Float, default=10.0)  # Kritik stok seviyesi
    unit_cost = Column(Float, default=0.0)
    supplier = Column(String(100), nullable=True)
    notes = Column(String(300), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Inventory {self.ingredient_name}: {self.quantity} {self.unit}>"
