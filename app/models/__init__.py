"""
Tüm modelleri tek noktadan erişilebilir yap
"""
from app.models.user import User, UserRole
from app.models.table import Table, TableStatus
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order, OrderStatus, PaymentStatus
from app.models.order_item import OrderItem, ItemStatus
from app.models.payment import Payment, PaymentMethod
from app.models.inventory import Inventory

__all__ = [
    "User", "UserRole",
    "Table", "TableStatus", 
    "Category",
    "Product",
    "Order", "OrderStatus", "PaymentStatus",
    "OrderItem", "ItemStatus",
    "Payment", "PaymentMethod",
    "Inventory"
]
