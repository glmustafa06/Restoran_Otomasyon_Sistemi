"""
Menü Yönetimi Router'ı
"""
from fastapi import APIRouter, Request, Depends, HTTPException, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category, Product
from app.routers.dashboard import get_current_user, require_role

from app.utils.templates import render_template
router = APIRouter(prefix="/menu", tags=["Menu"])
@router.get("/", response_class=HTMLResponse)

async def menu_page(request: Request, user = Depends(require_role("admin", "waiter")), db: Session = Depends(get_db)):
    """Menü yönetimi sayfası"""
    categories = db.query(Category).order_by(Category.sort_order).all()
    products = db.query(Product).order_by(Product.category_id, Product.name).all()

    return render_template("menu_management.html", {
        "request": request,
        "user": user,
        "categories": categories,
        "products": products
    })

@router.get("/api/categories")
async def list_categories(user = Depends(require_role("admin", "waiter")), db: Session = Depends(get_db)):
    """Tüm kategorileri döndürür"""
    categories = db.query(Category).order_by(Category.sort_order).all()
    return [{"id": c.id, "name": c.name, "sort_order": c.sort_order, "is_active": c.is_active} for c in categories]

@router.post("/api/categories/create")
async def create_category(name: str = Form(...), sort_order: int = Form(0), user = Depends(require_role("admin", "waiter")), db: Session = Depends(get_db)):
    """Yeni kategori oluşturur"""
    category = Category(name=name, sort_order=sort_order)
    db.add(category)
    db.commit()
    return {"success": True, "id": category.id}

@router.get("/api/products")
async def list_products(category_id: int = None, user = Depends(require_role("admin", "waiter")), db: Session = Depends(get_db)):
    """Ürünleri listeler"""
    query = db.query(Product)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    products = query.filter(Product.is_active == True).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "category_id": p.category_id,
            "category_name": p.category.name if p.category else "",
            "stock_quantity": p.stock_quantity,
            "is_active": p.is_active,
            "prep_time": p.prep_time
        }
        for p in products
    ]

@router.post("/api/products/create")
async def create_product(
    name: str = Form(...),
    category_id: int = Form(...),
    price: float = Form(...),
    description: str = Form(None),
    cost: float = Form(0),
    prep_time: int = Form(15),
    user = Depends(require_role("admin", "waiter")),
    db: Session = Depends(get_db)
):
    """Yeni ürün oluşturur"""
    product = Product(
        name=name,
        category_id=category_id,
        price=price,
        description=description,
        cost=cost,
        prep_time=prep_time
    )
    db.add(product)
    db.commit()
    return {"success": True, "id": product.id}

@router.post("/api/products/update/{product_id}")
async def update_product(
    product_id: int,
    name: str = Form(None),
    price: float = Form(None),
    is_active: str = Form(None),
    user = Depends(require_role("admin", "waiter")),
    db: Session = Depends(get_db)
):
    """Ürün günceller"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    if name:
        product.name = name
    if price is not None:
        product.price = price
    if is_active is not None:
        product.is_active = is_active.lower() in ["true", "1", "yes", "on"]

    db.commit()
    return {"success": True}
