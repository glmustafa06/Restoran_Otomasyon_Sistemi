"""
Restoran Otomasyon Sistemi - Ana Uygulama
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import SessionLocal, init_db
from app.utils.seed_data import seed_database

# Routers
from app.routers import (
    auth,
    dashboard,
    tables,
    orders,
    menu,
    kitchen,
    payments,
    inventory,
    reports
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başlangıç ve kapanış olayları"""

    # Veritabanını başlat
    init_db()

    db = SessionLocal()

    try:
        seed_database(db)

    except Exception as e:
        print(f"Seed data hatası (muhtemelen zaten var): {e}")

    finally:
        db.close()

    print("🚀 Restoran Otomasyon Sistemi başlatıldı!")

    yield

    print("👋 Sistem kapatılıyor...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Modern Restoran Yönetim Sistemi",
    version="1.0.0",
    lifespan=lifespan
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Router'ları ekle
# Prefixleri tekrar verme çünkü router içinde zaten var
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(tables.router)
app.include_router(orders.router)
app.include_router(menu.router)
app.include_router(kitchen.router)
app.include_router(payments.router)
app.include_router(inventory.router)
app.include_router(reports.router)


@app.get("/")
async def root():
    """Ana sayfa"""

    return RedirectResponse(url="/auth/login")


@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""

    return {
        "status": "ok",
        "app": settings.APP_NAME
    }