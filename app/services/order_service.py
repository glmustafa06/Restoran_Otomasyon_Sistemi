"""
Sipariş Servisi
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models import Order, OrderItem, OrderStatus, Table, TableStatus, Product

def create_new_order(db: Session, table_id: int, user_id: int, items: list, notes: str = None):
    """Yeni sipariş oluşturur"""
    # Sipariş oluştur
    order = Order(
        table_id=table_id,
        user_id=user_id,
        status=OrderStatus.PENDING,
        notes=notes
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Sipariş detaylarını ekle
    total = 0
    for item_data in items:
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        if product:
            quantity = item_data.get("quantity", 1)
            unit_price = product.price
            total_price = unit_price * quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                notes=item_data.get("notes", "")
            )
            db.add(order_item)
            total += total_price

    # Toplam tutarı güncelle
    order.total_amount = total
    order.final_amount = total

    # Masa durumunu güncelle
    table = db.query(Table).filter(Table.id == table_id).first()
    if table:
        table.status = TableStatus.OCCUPIED

    db.commit()
    return order

def get_active_orders(db: Session):
    """Aktif siparişleri getirir"""
    return db.query(Order).filter(Order.status != OrderStatus.PAID).order_by(Order.created_at.desc()).all()

def get_order_by_id(db: Session, order_id: int):
    """ID'ye göre sipariş getirir"""
    return db.query(Order).filter(Order.id == order_id).first()
