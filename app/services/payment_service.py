"""
Ödeme Servisi
"""
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Payment, PaymentMethod, Order, OrderStatus, PaymentStatus, Table, TableStatus

def process_order_payment(db: Session, order_id: int, amount: float, payment_method: PaymentMethod, tip: float = 0):
    """Sipariş için ödeme işlemi yapar"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None

    # Ödeme kaydı oluştur
    payment = Payment(
        order_id=order_id,
        amount=amount,
        payment_method=payment_method,
        tip=tip
    )
    db.add(payment)
    db.flush()

    # Toplam ödenen tutarı hesapla
    total_paid = sum(p.amount for p in order.payments)

    if total_paid >= order.final_amount:
        order.payment_status = PaymentStatus.PAID
        order.status = OrderStatus.PAID
        order.closed_at = datetime.now()

        # Masayı boşalt
        table = db.query(Table).filter(Table.id == order.table_id).first()
        if table:
            table.status = TableStatus.EMPTY
    else:
        order.payment_status = PaymentStatus.PARTIAL

    db.commit()
    return payment

def get_today_payments(db: Session):
    """Bugünkü ödemeleri getirir"""
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    return db.query(Payment).filter(Payment.created_at >= today_start).all()

def get_today_summary(db: Session):
    """Bugünkü özet istatistikleri getirir"""
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())

    payments = db.query(Payment).filter(Payment.created_at >= today_start).all()

    return {
        "total_sales": len(payments),
        "total_revenue": sum(p.amount for p in payments),
        "total_tips": sum(p.tip for p in payments)
    }
