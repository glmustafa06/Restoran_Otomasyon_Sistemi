"""
Stok Servisi
"""
from sqlalchemy.orm import Session
from app.models import Inventory

def get_low_stock_items(db: Session):
    """Kritik seviyenin altındaki stokları getirir"""
    return db.query(Inventory).filter(Inventory.quantity <= Inventory.min_stock).all()

def update_stock_quantity(db: Session, item_id: int, new_quantity: float):
    """Stok miktarını günceller"""
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if item:
        item.quantity = new_quantity
        db.commit()
        return item
    return None

def check_stock_availability(db: Session, ingredient_name: str, required_amount: float):
    """Stok yeterliliğini kontrol eder"""
    item = db.query(Inventory).filter(Inventory.ingredient_name == ingredient_name).first()
    if not item:
        return False
    return item.quantity >= required_amount
