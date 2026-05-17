"""
Stok / Envanter Router'ı
"""
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Inventory
from app.routers.dashboard import get_current_user, require_role

from app.utils.templates import render_template
router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)
@router.get("/", response_class=HTMLResponse)
async def inventory_page(request: Request, user = Depends(require_role("admin")), db: Session = Depends(get_db)):
    """Stok yönetimi sayfası"""
    items = db.query(Inventory).order_by(Inventory.ingredient_name).all()
    low_stock = db.query(Inventory).filter(Inventory.quantity <= Inventory.min_stock).all()

    return render_template("inventory.html", {
        "request": request,
        "user": user,
        "items": items,
        "low_stock": low_stock
    })

@router.get("/api/list")
async def list_inventory(user = Depends(require_role("admin")), db: Session = Depends(get_db)):
    """Tüm stok öğelerini döndürür"""
    items = db.query(Inventory).order_by(Inventory.ingredient_name).all()
    return [
        {
            "id": i.id,
            "ingredient_name": i.ingredient_name,
            "unit": i.unit,
            "quantity": i.quantity,
            "min_stock": i.min_stock,
            "is_low": i.quantity <= i.min_stock,
            "unit_cost": i.unit_cost,
            "supplier": i.supplier
        }
        for i in items
    ]

@router.post("/api/create")
async def create_inventory_item(
    ingredient_name: str = Form(...),
    unit: str = Form(...),
    quantity: float = Form(0),
    min_stock: float = Form(10),
    unit_cost: float = Form(0),
    supplier: str = Form(None),
    user = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Yeni stok öğesi oluşturur"""
    item = Inventory(
        ingredient_name=ingredient_name,
        unit=unit,
        quantity=quantity,
        min_stock=min_stock,
        unit_cost=unit_cost,
        supplier=supplier
    )
    db.add(item)
    db.commit()
    return {"success": True, "id": item.id}

@router.post("/api/update/{item_id}")
async def update_inventory(
    item_id: int,
    quantity: float = Form(None),
    min_stock: float = Form(None),
    user = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Stok günceller"""
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Öğe bulunamadı")

    if quantity is not None: item.quantity = quantity
    if min_stock is not None: item.min_stock = min_stock

    db.commit()
    return {"success": True, "is_low": item.quantity <= item.min_stock}
