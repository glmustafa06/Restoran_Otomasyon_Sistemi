"""
Veritabanı bağlantısı ve session yönetimi
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.config import settings

# SQLite için özel bağlantı argümanları
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args=connect_args,
    echo=False  # SQL sorgularını görmek istersen True yap
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency: Her istek için yeni DB session oluşturur"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Tüm tabloları oluşturur"""
    from app.models import user, table, category, product, order, order_item, inventory, payment
    Base.metadata.create_all(bind=engine)
