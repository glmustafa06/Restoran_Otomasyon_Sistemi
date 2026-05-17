"""
Kategori Modeli
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    # İlişki: Bir kategorinin birden fazla ürünü olabilir
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"
