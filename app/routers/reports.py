"""
Raporlar Router'ı
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.models import Order, Payment, Product, OrderItem
from app.routers.dashboard import get_current_user, require_role

from app.utils.templates import render_template
router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)
@router.get("/", response_class=HTMLResponse)
async def reports_page(request: Request, user = Depends(require_role("admin", "cashier")), db: Session = Depends(get_db)):
    """Raporlar sayfası"""
    return render_template("reports.html", {
        "request": request,
        "user": user
    })

@router.get("/api/sales")
async def sales_report(period: str = "today", user = Depends(require_role("admin", "cashier")), db: Session = Depends(get_db)):
    """Satış raporu"""
    today = datetime.now().date()

    if period == "today":
        start = datetime.combine(today, datetime.min.time())
    elif period == "week":
        start = datetime.combine(today - timedelta(days=7), datetime.min.time())
    elif period == "month":
        start = datetime.combine(today - timedelta(days=30), datetime.min.time())
    else:
        start = datetime.combine(today, datetime.min.time())

    orders = db.query(Order).filter(Order.created_at >= start).all()

    total_orders = len(orders)
    total_revenue = sum(o.final_amount for o in orders)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    return {
        "period": period,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "avg_order_value": round(avg_order_value, 2)
    }

@router.get("/api/popular-products")
async def popular_products(limit: int = 10, user = Depends(require_role("admin", "cashier")), db: Session = Depends(get_db)):
    """En popüler ürünler"""
    results = db.query(
        Product.name,
        func.sum(OrderItem.quantity).label("total_sold")
    ).join(OrderItem).group_by(Product.id).order_by(func.sum(OrderItem.quantity).desc()).limit(limit).all()

    return [
        {"name": r.name, "total_sold": r.total_sold or 0}
        for r in results
    ]
