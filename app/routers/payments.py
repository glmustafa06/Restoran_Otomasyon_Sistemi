"""
Kasa / Ödeme Router'ı
"""
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Order, OrderItem, OrderStatus, PaymentStatus, Payment, PaymentMethod, Table, TableStatus
from app.routers.dashboard import get_current_user, require_role

from app.utils.templates import render_template
router = APIRouter(prefix="/payments", tags=["Payments"])
@router.get("/", response_class=HTMLResponse)
async def payments_page(request: Request, user = Depends(require_role("admin", "cashier")), db: Session = Depends(get_db)):
    """Kasa sayfası"""
    # Ödenmemiş siparişler
    unpaid_orders = db.query(Order).filter(
        Order.payment_status != PaymentStatus.PAID
    ).order_by(Order.created_at.desc()).all()

    # Bugünkü ödemeler
    today = datetime.now().date()
    today_payments = db.query(Payment).filter(
        Payment.created_at >= datetime.combine(today, datetime.min.time())
    ).all()

    return render_template("payments.html", {
        "request": request,
        "user": user,
        "unpaid_orders": unpaid_orders,
        "today_payments": today_payments,
        "PaymentMethod": PaymentMethod,
        "PaymentStatus": PaymentStatus
    })

@router.get("/order/{order_id}", response_class=HTMLResponse)
async def payment_detail(order_id: int, request: Request, user = Depends(require_role("admin", "cashier")), db: Session = Depends(get_db)):
    """Ödeme detay sayfası"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")

    return render_template("payment_detail.html", {
        "request": request,
        "user": user,
        "order": order,
        "PaymentMethod": PaymentMethod
    })

@router.post("/api/process/{order_id}")
async def process_payment(
    order_id: int,
    amount: float = Form(...),
    payment_method: str = Form(...),
    tip: float = Form(0),
    user = Depends(require_role("admin", "cashier")),
    db: Session = Depends(get_db)
):
    """Ödeme işlemi"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")

    # Ödeme kaydı oluştur
    payment = Payment(
        order_id=order_id,
        amount=amount,
        payment_method=PaymentMethod(payment_method),
        tip=tip
    )
    db.add(payment)

    # Sipariş durumunu güncelle
    total_paid = sum(p.amount for p in order.payments) + amount

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

    return {
        "success": True,
        "message": "Ödeme başarılı",
        "remaining": max(0, order.final_amount - total_paid)
    }

@router.get("/api/today-summary")
async def today_summary(user = Depends(require_role("admin", "cashier")), db: Session = Depends(get_db)):
    """Bugünkü özet"""
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())

    payments = db.query(Payment).filter(Payment.created_at >= today_start).all()
    total_sales = len(payments)
    total_revenue = sum(p.amount for p in payments)
    total_tips = sum(p.tip for p in payments)

    paid_order_ids = {p.order_id for p in payments}
    cost_items = db.query(OrderItem).join(Order).filter(Order.id.in_(paid_order_ids)).all() if paid_order_ids else []
    total_cost = sum(item.quantity * (item.product.cost if item.product else 0) for item in cost_items)
    net_profit = total_revenue - total_cost

    return {
        "total_sales": total_sales,
        "total_revenue": total_revenue,
        "total_tips": total_tips,
        "total_cost": total_cost,
        "net_profit": net_profit
    }
