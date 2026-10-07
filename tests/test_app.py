from app.main import app


def test_health():
    r = app.test_client().get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_customers():
    r = app.test_client().get("/customers")
    assert len(r.get_json()) == 3


def test_sales_summary():
    r = app.test_client().get("/sales/summary")
    assert r.get_json()["total"] == 3440.75
