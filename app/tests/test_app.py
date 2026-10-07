import pytest
from sqlalchemy import create_engine, text

from app import db
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    url = f"sqlite:///{tmp_path}/test.db"
    monkeypatch.setenv("DATABASE_URL", url)
    db._engine = None
    engine = create_engine(url)
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, region TEXT)"))
        conn.execute(text("CREATE TABLE sales (customer_id INTEGER, amount NUMERIC)"))
        conn.execute(text("INSERT INTO customers VALUES (1, 'Test A', 'South'), (2, 'Test B', 'North')"))
        conn.execute(text("INSERT INTO sales VALUES (1, 100.5), (1, 50), (2, 25)"))
    return app.test_client()


def test_health():
    r = app.test_client().get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_customers(client):
    r = client.get("/customers")
    assert r.status_code == 200
    assert len(r.get_json()) == 2


def test_sales_summary(client):
    data = client.get("/sales/summary").get_json()
    assert data["total"] == 175.5
    assert data["by_customer"][0] == {"customer_id": 1, "total": 150.5}


def test_database_not_configured(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    r = app.test_client().get("/customers")
    assert r.status_code == 503
