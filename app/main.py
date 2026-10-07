from flask import Flask, jsonify

app = Flask(__name__)

# Sample company data (replace with a real DB such as Azure SQL / PostgreSQL later)
CUSTOMERS = [
    {"id": 1, "name": "Acme Corp", "region": "South"},
    {"id": 2, "name": "Globex", "region": "North"},
    {"id": 3, "name": "Initech", "region": "South"},
]
SALES = [
    {"customer_id": 1, "amount": 1200.50},
    {"customer_id": 2, "amount": 800.00},
    {"customer_id": 1, "amount": 450.25},
    {"customer_id": 3, "amount": 990.00},
]


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/customers")
def customers():
    return jsonify(CUSTOMERS)


@app.get("/sales/summary")
def sales_summary():
    total = round(sum(s["amount"] for s in SALES), 2)
    by_customer = {}
    for s in SALES:
        by_customer[s["customer_id"]] = round(by_customer.get(s["customer_id"], 0) + s["amount"], 2)
    return jsonify(total=total, by_customer=by_customer)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
