"""
Temel Testler
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Sağlık kontrolü endpoint'ini test eder"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_login_page():
    """Login sayfasının yüklendiğini test eder"""
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert "Giriş" in response.text

def test_root_redirect():
    """Ana sayfanın login'e yönlendirdiğini test eder"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/auth/login" in response.headers["location"]
