"""
Masa Yönetimi Router'ı
"""
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Table, TableStatus, Order, OrderStatus
from app.routers.dashboard import get_current_user, require_role

from app.utils.templates import render_template
router = APIRouter(prefix="/tables", tags=["Tables"])

@router.get("/", response_class=HTMLResponse)
async def tables_page(request: Request, user = Depends(require_role("admin", "waiter")), db: Session = Depends(get_db)):
    """Masa yönetimi sayfası"""
    tables = db.query(Table).order_by(Table.section, Table.table_number).all()
    sections = db.query(Table.section).distinct().all()
    sections = [s[0] for s in sections]

    return render_template("tables.html", {
        "request": request,
        "user": user,
        "tables": tables,
        "sections": sections,
        "TableStatus": TableStatus
    })

@router.get("/api/list")
async def list_tables(user = Depends(require_role("admin", "waiter")), db: Session = Depends(get_db)):
    """Tüm masaları JSON olarak döndürür"""
    tables = db.query(Table).all()
    return [
        {
            "id": t.id,
            "table_number": t.table_number,
            "section": t.section,
            "capacity": t.capacity,
            "status": t.status.value,
            "position_x": t.position_x,
            "position_y": t.position_y
        }
        for t in tables
    ]

@router.post("/api/update-status/{table_id}")
async def update_table_status(table_id: int, status: str = Form(...), user = Depends(require_role("admin", "waiter")), db: Session = Depends(get_db)):
    """Masa durumunu günceller"""
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Masa bulunamadı")

    try:
        table.status = TableStatus(status)
        db.commit()
        return {"success": True, "message": f"Masa {table.table_number} durumu güncellendi"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Geçersiz durum")

@router.get("/api/status-counts")
async def table_status_counts(db: Session = Depends(get_db)):
    """Masa durum sayımları"""
    counts = {}
    for status in TableStatus:
        counts[status.value] = db.query(Table).filter(Table.status == status).count()
    return counts
