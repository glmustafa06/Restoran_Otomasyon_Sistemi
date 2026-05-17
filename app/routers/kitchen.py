"""
Mutfak Ekranı Router'ı
"""
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/kitchen",
    tags=["Kitchen"]
)
from app.database import get_db
from app.models import Order, OrderItem, OrderStatus, ItemStatus
from app.routers.dashboard import get_current_user, require_role

from app.utils.templates import render_template

@router.get("/", response_class=HTMLResponse)
async def kitchen_page(request: Request, user = Depends(require_role("admin", "chef")), db: Session = Depends(get_db)):
    """Mutfak ekranı"""
    # Bekleyen ve hazırlanan siparişler
    pending_items = db.query(OrderItem).join(Order).filter(
        OrderItem.status.in_([ItemStatus.PENDING, ItemStatus.PREPARING])
    ).order_by(Order.created_at).all()

    return render_template("kitchen_display.html", {
        "request": request,
        "user": user,
        "pending_items": pending_items,
        "ItemStatus": ItemStatus
    })

@router.get("/api/orders")
async def kitchen_orders(user = Depends(require_role("admin", "chef")), db: Session = Depends(get_db)):
    """Mutfak için siparişleri döndürür"""
    orders = db.query(Order).filter(
        Order.status.in_([OrderStatus.PENDING, OrderStatus.PREPARING])
    ).order_by(Order.created_at).all()

    result = []
    for order in orders:
        items = []
        for item in order.items:
            if item.status in [ItemStatus.PENDING, ItemStatus.PREPARING]:
                items.append({
                    "id": item.id,
                    "product_name": item.product.name if item.product else "",
                    "quantity": item.quantity,
                    "notes": item.notes,
                    "status": item.status.value,
                    "prep_time": item.product.prep_time if item.product else 15
                })

        if items:
            result.append({
                "order_id": order.id,
                "table_number": order.table.table_number if order.table else "",
                "created_at": order.created_at.strftime("%H:%M") if order.created_at else "",
                "items": items,
                "notes": order.notes
            })

    return result

@router.post("/api/item-status/{item_id}")
async def update_item_status(item_id: int, status: str = Form(...), user = Depends(require_role("admin", "chef")), db: Session = Depends(get_db)):
    """Sipariş öğesi durumunu günceller"""
    item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Öğe bulunamadı")

    try:
        item.status = ItemStatus(status)
        db.commit()

        # Tüm öğeler hazırsa sipariş durumunu güncelle
        order = item.order
        all_ready = all(i.status == ItemStatus.READY for i in order.items)
        if all_ready:
            order.status = OrderStatus.READY
            db.commit()

        return {"success": True}
    except ValueError:
        raise HTTPException(status_code=400, detail="Geçersiz durum")
