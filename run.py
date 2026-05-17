#!/usr/bin/env python3
"""Restoran Otomasyon Sistemi Başlatıcı"""
import os
from pathlib import Path
import threading
import time
import webbrowser
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("🍽️  Restoran Otomasyon Sistemi başlatılıyor...")
    print("📱 Tarayıcı otomatik açılacak...")
    print("⏳ Lütfen bekleyin...")

    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
