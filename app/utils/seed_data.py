"""
Örnek/Demo veri oluşturma
"""
from sqlalchemy.orm import Session
from app.database import Base, engine
from app.models import User, UserRole, Table, TableStatus, Category, Product, Inventory, Order, OrderItem, Payment, PaymentMethod, OrderStatus, PaymentStatus
from app.utils.security import hash_password
from datetime import datetime


def seed_database(db: Session):
    """Veritabanına örnek veriler ekler"""

    # Kullanıcılar
    users = [
        User(username="admin", full_name="Sistem Yöneticisi", 
             password_hash=hash_password("admin123"), role=UserRole.ADMIN),
        User(username="garson1", full_name="Ahmet Yılmaz", 
             password_hash=hash_password("garson123"), role=UserRole.WAITER),
        User(username="asci1", full_name="Mehmet Kaya", 
             password_hash=hash_password("asci123"), role=UserRole.CHEF),
        User(username="kasiyer1", full_name="Ayşe Demir", 
             password_hash=hash_password("kasiyer123"), role=UserRole.CASHIER),
    ]

    for user in users:
        existing_user = db.query(User).filter(User.username == user.username).first()
        if not existing_user:
            db.add(user)
    db.commit()

    # Masalar
    tables = [
        Table(table_number="M1", section="İç Mekan", capacity=4, position_x=50, position_y=50),
        Table(table_number="M2", section="İç Mekan", capacity=4, position_x=150, position_y=50),
        Table(table_number="M3", section="İç Mekan", capacity=6, position_x=250, position_y=50),
        Table(table_number="M4", section="İç Mekan", capacity=2, position_x=350, position_y=50),
        Table(table_number="B1", section="Bahçe", capacity=4, position_x=50, position_y=150),
        Table(table_number="B2", section="Bahçe", capacity=6, position_x=150, position_y=150),
        Table(table_number="U1", section="Üst Kat", capacity=4, position_x=50, position_y=250),
        Table(table_number="U2", section="Üst Kat", capacity=8, position_x=150, position_y=250),
    ]

    for table in tables:
        existing_table = db.query(Table).filter(Table.table_number == table.table_number).first()
        if not existing_table:
            db.add(table)
    db.commit()

    # Kategoriler
    categories = [
        Category(name="Başlangıçlar", sort_order=1),
        Category(name="Ana Yemekler", sort_order=2),
        Category(name="Tatlılar", sort_order=3),
        Category(name="İçecekler", sort_order=4),
        Category(name="Fast Food", sort_order=5),
    ]

    for cat in categories:
        existing_cat = db.query(Category).filter(Category.name == cat.name).first()
        if not existing_cat:
            db.add(cat)
    db.commit()

    # Ürünler
    products = [
        Product(category_id=1, name="Mercimek Çorbası", description="Geleneksel mercimek çorbası",
                price=45.0, cost=15.0, prep_time=10, stock_quantity=100),
        Product(category_id=1, name="Sigara Böreği", description="5 adet sigara böreği",
                price=55.0, cost=20.0, prep_time=12, stock_quantity=50),
        Product(category_id=2, name="Izgara Köfte", description="180gr köfte, pilav, salata",
                price=120.0, cost=45.0, prep_time=20, stock_quantity=30),
        Product(category_id=2, name="Tavuk Şiş", description="Marine edilmiş tavuk göğsü",
                price=110.0, cost=40.0, prep_time=18, stock_quantity=40),
        Product(category_id=2, name="Kuzu Tandır", description="7 saat pişmiş kuzu tandır",
                price=180.0, cost=80.0, prep_time=30, stock_quantity=15),
        Product(category_id=3, name="Sütlaç", description="Fırın sütlaç",
                price=40.0, cost=12.0, prep_time=5, stock_quantity=25),
        Product(category_id=3, name="Baklava", description="4 dilim baklava",
                price=60.0, cost=25.0, prep_time=3, stock_quantity=20),
        Product(category_id=4, name="Türk Kahvesi", description="Traditional Turkish coffee",
                price=25.0, cost=5.0, prep_time=5, stock_quantity=-1),
        Product(category_id=4, name="Çay", description="Demli çay",
                price=10.0, cost=2.0, prep_time=3, stock_quantity=-1),
        Product(category_id=4, name="Ayran", description="1 lt ayran",
                price=15.0, cost=5.0, prep_time=2, stock_quantity=-1),
        Product(category_id=5, name="Hamburger", description="150gr burger, patates, içecek",
                price=95.0, cost=35.0, prep_time=15, stock_quantity=40),
        Product(category_id=5, name="Pizza Margherita", description="Mozzarella, domates, fesleğen",
                price=85.0, cost=30.0, prep_time=20, stock_quantity=35),
    ]

    for product in products:
        existing_product = db.query(Product).filter(Product.name == product.name).first()
        if not existing_product:
            db.add(product)
    db.commit()

    # Inventory
    inventory_items = [
        Inventory(ingredient_name="Mercimek", unit="kg", quantity=18.0, min_stock=10.0, unit_cost=35.0, supplier="Anadolu Gıda", notes="Çorba için"),
        Inventory(ingredient_name="Yufka", unit="adet", quantity=80.0, min_stock=20.0, unit_cost=0.8, supplier="Ege Tedarik", notes="Sigara böreği için"),
        Inventory(ingredient_name="Köfte Eti", unit="kg", quantity=25.0, min_stock=8.0, unit_cost=70.0, supplier="Kasap A.Ş.", notes="Izgara köfte için"),
        Inventory(ingredient_name="Tavuk Göğsü", unit="kg", quantity=18.0, min_stock=10.0, unit_cost=55.0, supplier="Piliç Tedarik", notes="Tavuk şiş için"),
        Inventory(ingredient_name="Kuzu Eti", unit="kg", quantity=12.0, min_stock=5.0, unit_cost=120.0, supplier="Küçük Çiftlik", notes="Kuzu tandır için"),
        Inventory(ingredient_name="Süt", unit="lt", quantity=50.0, min_stock=15.0, unit_cost=8.0, supplier="Süt Kooperatifi", notes="Tatlılar için"),
        Inventory(ingredient_name="Baklava Hamuru", unit="adet", quantity=30.0, min_stock=10.0, unit_cost=3.5, supplier="Tatlıcılar", notes="Baklava için"),
        Inventory(ingredient_name="Mozzarella", unit="kg", quantity=12.0, min_stock=5.0, unit_cost=90.0, supplier="Peynirci", notes="Pizza için"),
        Inventory(ingredient_name="Domates", unit="kg", quantity=22.0, min_stock=10.0, unit_cost=20.0, supplier="Sebze Pazarı", notes="Salata ve pizza için"),
        Inventory(ingredient_name="Patates", unit="kg", quantity=45.0, min_stock=15.0, unit_cost=18.0, supplier="Sebze Pazarı", notes="Hamburger için"),
    ]
    for item in inventory_items:
        existing_item = db.query(Inventory).filter(Inventory.ingredient_name == item.ingredient_name).first()
        if not existing_item:
            db.add(item)
    db.commit()

    # Örnek siparişler ve ödemeler
    if db.query(Order).count() == 0:
        admin_user = db.query(User).filter(User.username == 'admin').first()
        waiter_user = db.query(User).filter(User.username == 'garson1').first()
        table_m1 = db.query(Table).filter(Table.table_number == 'M1').first()
        product_kofte = db.query(Product).filter(Product.name == 'Izgara Köfte').first()
        product_cay = db.query(Product).filter(Product.name == 'Çay').first()
        if waiter_user and table_m1 and product_kofte and product_cay:
            order = Order(
                table_id=table_m1.id,
                user_id=waiter_user.id,
                status=OrderStatus.PAID,
                payment_status=PaymentStatus.PAID,
                total_amount=130.0,
                final_amount=130.0,
                notes='Acılı olsun',
                created_at=datetime.now()
            )
            db.add(order)
            db.commit()
            db.refresh(order)
            db.add(OrderItem(order_id=order.id, product_id=product_kofte.id, quantity=1, unit_price=product_kofte.price, total_price=product_kofte.price, notes='Az tuzlu'))
            db.add(OrderItem(order_id=order.id, product_id=product_cay.id, quantity=1, unit_price=product_cay.price, total_price=product_cay.price, notes=''))
            db.add(Payment(order_id=order.id, amount=130.0, payment_method=PaymentMethod.CASH, tip=10.0, receipt_number='FAT-001', notes='Nakit ödeme', created_at=datetime.now()))
            table_m1.status = TableStatus.EMPTY
            db.commit()

    print("✅ Örnek veriler başarıyla yüklendi!")
