"""
Dashboard Router'ı
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User, Order, Table, Product, Inventory, OrderStatus, PaymentStatus
from app.utils.security import decode_access_token

from app.utils.templates import render_template
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Cookie'den kullanıcı bilgisini alır"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Oturum açık değil")

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Geçersiz token")

    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")

    return user


def require_role(*allowed_roles):
    def dependency(user: User = Depends(get_current_user)):
        allowed = [r.value if hasattr(r, 'value') else r for r in allowed_roles]
        if user.role.value not in allowed:
            raise HTTPException(status_code=403, detail="Bu sayfaya erişim yetkiniz yok")
        return user
    return dependency


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Ana dashboard sayfası"""

    # İstatistikler
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())

    stats = {
        "total_orders_today": db.query(Order).filter(Order.created_at >= today_start).count(),
        "active_orders": db.query(Order).filter(Order.status.notin_([OrderStatus.PAID, OrderStatus.CANCELLED])).count(),
        "total_revenue_today": db.query(func.sum(Order.final_amount)).filter(
            Order.created_at >= today_start, Order.payment_status == PaymentStatus.PAID
        ).scalar() or 0,
        "active_tables": db.query(Table).filter(Table.status == "occupied").count(),
        "total_tables": db.query(Table).count(),
        "low_stock_items": db.query(Inventory).filter(Inventory.quantity <= Inventory.min_stock).count()
    }

    # Son siparişler
    recent_orders = db.query(Order).order_by(Order.created_at.desc()).limit(5).all()

    # Popüler ürünler (bugün)
    popular_products = []  # İleride eklenecek

    return render_template("dashboard.html", {
        "request": request,
        "user": user,
        "stats": stats,
        "recent_orders": recent_orders,
        "popular_products": popular_products,
        "app_name": "Restoran Otomasyon Sistemi"
    })
