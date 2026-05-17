"""
Ürün Schema'ları
"""
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    cost: float = 0
    category_id: int
    prep_time: int = 15
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    category_name: Optional[str] = None

    class Config:
        from_attributes = True
