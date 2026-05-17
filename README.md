# 🍽️ Restoran Otomasyon Sistemi

Modern, web tabanlı restoran yönetim sistemi.

## 🚀 Özellikler

- ✅ Masa Yönetimi (Görsel salon planı)
- ✅ Sipariş Alma (Kategori/ürün bazlı)
- ✅ Mutfak Ekranı (Anlık sipariş takibi)
- ✅ Kasa/Ödeme (Nakit, Kart, Mobil)
- ✅ Stok/Envanter Yönetimi
- ✅ Raporlar ve Analizler
- ✅ Çoklu kullanıcı rolleri (Admin, Garson, Aşçı, Kasiyer)
- ✅ Gerçek zamanlı güncellemeler

## 🛠️ Teknolojiler

- **Backend:** Python + FastAPI
- **Frontend:** HTML + Tailwind CSS + Vanilla JS
- **Veritabanı:** SQLite (SQLAlchemy ORM)
- **Güvenlik:** JWT Token + Bcrypt

## 📦 Kurulum

```bash
# 1. Sanal ortam oluştur
python -m venv venv

# 2. Aktif et (Windows)
.\venv\Scripts\activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Çalıştır
python run.py
```

## 🔑 Varsayılan Giriş Bilgileri

| Kullanıcı | Şifre | Rol |
|-----------|-------|-----|
| admin | admin123 | Yönetici |
| garson1 | garson123 | Garson |
| ascı1 | ascı123 | Aşçı |
| kasiyer1 | kasiyer123 | Kasiyer |

## 📁 Proje Yapısı

```
restoran_otomasyon_sistemi/
├── app/                    # Ana uygulama
│   ├── main.py             # FastAPI giriş
│   ├── config.py           # Ayarlar
│   ├── database.py         # DB bağlantısı
│   ├── models/             # Veritabanı modelleri
│   ├── schemas/            # Veri doğrulama
│   ├── routers/            # API endpoint'leri
│   ├── services/           # İş mantığı
│   └── utils/              # Yardımcılar
├── templates/              # HTML şablonları
├── static/                 # CSS, JS, resimler
├── tests/                  # Testler
├── requirements.txt        # Bağımlılıklar
└── run.py                  # Başlatıcı
```

## 🌐 Erişim

Tarayıcıda: `http://127.0.0.1:8000`

---
**Hazırlayan:** Restoran Otomasyon Sistemi
