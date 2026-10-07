from flask import Flask, jsonify

from app.db import DatabaseNotConfigured, query

app = Flask(__name__)


@app.errorhandler(DatabaseNotConfigured)
def database_not_configured(_error):
    return jsonify(error="DATABASE_URL is not configured"), 503


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/customers")
def customers():
    rows = query("SELECT id, name, region FROM customers ORDER BY id")
    return jsonify(rows)


@app.get("/sales/summary")
def sales_summary():
    total = query("SELECT COALESCE(SUM(amount), 0) AS total FROM sales")[0]["total"]
    by_customer = query(
        "SELECT customer_id, SUM(amount) AS total FROM sales GROUP BY customer_id ORDER BY customer_id"
    )
    return jsonify(
        total=round(float(total), 2),
        by_customer=[
            {"customer_id": r["customer_id"], "total": round(float(r["total"]), 2)}
            for r in by_customer
        ],
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
