"""
Ürün (Menü Öğesi) Modeli
"""
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    cost = Column(Float, default=0.0)  # Maliyet (kar hesabı için)
    image_url = Column(String(255), nullable=True)
    stock_quantity = Column(Integer, default=0)  # -1 ise sınırsız
    is_active = Column(Boolean, default=True)
    prep_time = Column(Integer, default=15)  # Hazırlama süresi (dakika)

    # İlişki: Her ürün bir kategoriye aittir
    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product {self.name} ({self.price}₺)>"
