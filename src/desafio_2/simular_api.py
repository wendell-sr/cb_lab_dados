from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/api/getGuestChecks", methods=["GET"])
def get_guest_checks():
    store_id = request.args.get("storeId")
    date = request.args.get("date")
    if not store_id or not date:
        return jsonify({"error": "Parâmetros 'storeId' e 'date' são obrigatórios"}), 400
    return jsonify({
        "storeId": store_id,
        "date": date,
        "guestChecks": [
            {"id": 1, "subtotal": 100.0, "total": 120.0},
            {"id": 2, "subtotal": 200.0, "total": 240.0}
        ]
    })

@app.route("/api/getTransactions", methods=["GET"])
def get_transactions():
    store_id = request.args.get("storeId")
    date = request.args.get("date")
    if not store_id or not date:
        return jsonify({"error": "Parâmetros 'storeId' e 'date' são obrigatórios"}), 400
    return jsonify({
        "storeId": store_id,
        "date": date,
        "transactions": [
            {"id": 1, "method": "cash", "amount": 120.0},
            {"id": 2, "method": "card", "amount": 240.0}
        ]
    })

@app.route("/api/getFiscalInvoice", methods=["GET"])
def get_fiscal_invoice():
    store_id = request.args.get("storeId")
    date = request.args.get("date")
    if not store_id or not date:
        return jsonify({"error": "Parâmetros 'storeId' e 'date' são obrigatórios"}), 400
    return jsonify({
        "storeId": store_id,
        "date": date,
        "invoices": [
            {"id": 1, "amount": 120.0, "tax": 20.0},
            {"id": 2, "amount": 240.0, "tax": 40.0}
        ]
    })

@app.route("/api/getChargeBack", methods=["GET"])
def get_charge_back():
    store_id = request.args.get("storeId")
    date = request.args.get("date")
    if not store_id or not date:
        return jsonify({"error": "Parâmetros 'storeId' e 'date' são obrigatórios"}), 400
    return jsonify({
        "storeId": store_id,
        "date": date,
        "chargeBacks": [
            {"id": 1, "reason": "Duplicate transaction", "amount": -50.0},
            {"id": 2, "reason": "Customer dispute", "amount": -30.0}
        ]
    })

@app.route("/api/getCashManagementDetails", methods=["GET"])
def get_cash_management_details():
    store_id = request.args.get("storeId")
    date = request.args.get("date")
    if not store_id or not date:
        return jsonify({"error": "Parâmetros 'storeId' e 'date' são obrigatórios"}), 400
    return jsonify({
        "storeId": store_id,
        "date": date,
        "cashManagement": [
            {"id": 1, "cashIn": 500.0, "cashOut": 200.0},
            {"id": 2, "cashIn": 700.0, "cashOut": 300.0}
        ]
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
