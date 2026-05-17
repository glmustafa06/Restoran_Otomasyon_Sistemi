"""
Uygulama ayarları ve yapılandırma
"""
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Uygulama
    APP_NAME: str = "Restoran Otomasyon Sistemi"
    DEBUG: bool = True

    # Veritabanı
    DATABASE_URL: str = "sqlite:///./database.db"

    # Güvenlik
    SECRET_KEY: str = "restoran-super-gizli-anahtar-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 saat

    # Restoran Ayarları
    CURRENCY: str = "₺"
    TAX_RATE: float = 0.08  # %8 KDV
    SERVICE_FEE: float = 0.0  # Servis bedeli

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
