"""
Genel yardımcı fonksiyonlar
"""
from datetime import datetime

def format_currency(amount: float) -> str:
    """Tutarı para birimi formatında döndürür"""
    return f"{amount:,.2f} ₺"

def format_datetime(dt: datetime) -> str:
    """Tarihi okunabilir formatta döndürür"""
    if dt:
        return dt.strftime("%d.%m.%Y %H:%M")
    return "-"

def format_time(dt: datetime) -> str:
    """Sadece saati döndürür"""
    if dt:
        return dt.strftime("%H:%M")
    return "-"

def calculate_tax(amount: float, tax_rate: float = 0.08) -> float:
    """KDV hesaplar"""
    return amount * tax_rate

def calculate_total_with_tax(amount: float, tax_rate: float = 0.08) -> float:
    """KDV dahil toplam tutar"""
    return amount + calculate_tax(amount, tax_rate)
