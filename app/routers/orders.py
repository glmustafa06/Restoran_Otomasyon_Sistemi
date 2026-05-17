"""
Sipariş Yönetimi Router'ı
"""
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.database import get_db
from app.models import Order, OrderItem, OrderStatus, ItemStatus, Table, Product, User, TableStatus, Category
from app.routers.dashboard import get_current_user, require_role

from app.utils.templates import render_template
router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_class=HTMLResponse)
async def orders_page(request: Request, user = Depends(require_role("admin", "waiter")), db: Session = Depends(get_db)):
    """Sipariş sayfası"""
    # Aktif siparişler
    active_orders = db.query(Order).filter(Order.status.notin_([OrderStatus.PAID, OrderStatus.CANCELLED])).order_by(Order.created_at.desc()).all()

    # Boş masalar (yeni sipariş için)
    available_tables = db.query(Table).filter(Table.status == "empty").all()

    # Ürünler ve kategoriler
    products = db.query(Product).filter(Product.is_active == True).all()
    categories = db.query(Category).order_by(Category.name).all()

    return render_template("orders.html", {
        "request": request,
        "user": user,
        "active_orders": active_orders,
        "available_tables": available_tables,
        "products": products,
        "categories": categories,
        "OrderStatus": OrderStatus
    })

@router.get("/new/{table_id}", response_class=HTMLResponse)
async def new_order_page(table_id: int, request: Request, user = Depends(require_role("admin", "waiter")), db: Session = Depends(get_db)):
    """Yeni sipariş sayfası"""
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Masa bulunamadı")

    products = db.query(Product).filter(Product.is_active == True).order_by(Product.category_id).all()

    return render_template("order_form.html", {
        "request": request,
        "user": user,
        "table": table,
        "products": products
    })

@router.post("/api/create")
async def create_order(
    table_id: int = Form(...),
    items: str = Form(...),  # JSON formatında: [{"product_id": 1, "quantity": 2, "notes": ""}]
    notes: str = Form(None),
    user = Depends(require_role("admin", "waiter")),
    db: Session = Depends(get_db)
):
    """Yeni sipariş oluşturur"""
    import json

    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Masa bulunamadı")

    # Yeni sipariş oluştur
    order = Order(
        table_id=table_id,
        user_id=user.id,
        status=OrderStatus.PENDING,
        notes=notes
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Sipariş detaylarını ekle
    items_list = json.loads(items)
    total = 0

    for item_data in items_list:
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
    table.status = TableStatus.OCCUPIED

    db.commit()

    return {"success": True, "order_id": order.id, "total": total}

@router.get("/api/active")
async def active_orders(user = Depends(require_role("admin", "waiter")), db: Session = Depends(get_db)):
    """Aktif siparişleri döndürür"""
    orders = db.query(Order).filter(Order.status.notin_([OrderStatus.PAID, OrderStatus.CANCELLED])).order_by(Order.created_at.desc()).all()
    return [
        {
            "id": o.id,
            "table_id": o.table_id,
            "table_number": o.table.table_number if o.table else "",
            "status": o.status.value,
            "total_amount": o.total_amount,
            "final_amount": o.final_amount,
            "created_at": o.created_at.strftime("%H:%M") if o.created_at else "",
            "item_count": len(o.items)
        }
        for o in orders
    ]

@router.get("/api/detail/{order_id}")
async def order_detail(order_id: int, user = Depends(require_role("admin", "waiter")), db: Session = Depends(get_db)):
    """Sipariş detaylarını döndürür"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")

    return {
        "id": order.id,
        "table_number": order.table.table_number if order.table else "",
        "status": order.status.value,
        "total_amount": order.total_amount,
        "final_amount": order.final_amount,
        "notes": order.notes,
        "items": [
            {
                "id": item.id,
                "product_name": item.product.name if item.product else "",
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
                "status": item.status.value,
                "notes": item.notes
            }
            for item in order.items
        ]
    }
