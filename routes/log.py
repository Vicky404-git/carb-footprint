# routes/log.py
from flask import Blueprint, request, jsonify
from models import db, ActivityLog
from data.emission_factors import FACTORS, MAX_QTY
from datetime import date

log_bp = Blueprint("log", __name__)

@log_bp.route("/log", methods=["POST"])
def log_activity():
    data = request.get_json()
    category = data.get("category")
    activity  = data.get("activity")
    quantity  = data.get("quantity")

    if not all([category, activity, quantity is not None]):
        return jsonify({"error": "category, activity, quantity required"}), 400

    try:
        quantity = float(quantity)
    except (ValueError, TypeError):
        return jsonify({"error": "quantity must be a number"}), 400

    if quantity <= 0:
        return jsonify({"error": "quantity must be positive"}), 400

    if category not in FACTORS:
        return jsonify({"error": f"unknown category: {category}"}), 400

    if activity not in FACTORS[category]:
        return jsonify({"error": f"unknown activity: {activity}"}), 400

    max_q = MAX_QTY.get(category, 10000)
    if quantity > max_q:
        return jsonify({"error": f"quantity too high — max {max_q} for {category}"}), 400

    co2 = round(FACTORS[category][activity] * quantity, 4)

    entry = ActivityLog(
        date=date.today(),
        category=category,
        activity=activity,
        quantity=quantity,
        co2_kg=co2
    )
    db.session.add(entry)
    db.session.commit()

    return jsonify({
        "message": "logged",
        "id":       entry.id,
        "co2_kg":   co2,
        "category": category,
        "activity": activity,
        "quantity": quantity
    }), 201


@log_bp.route("/log/<int:log_id>", methods=["DELETE"])
def delete_log(log_id):
    entry = db.get_or_404(ActivityLog, log_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "deleted", "id": log_id}), 200


@log_bp.route("/log/<int:log_id>", methods=["PUT"])
def edit_log(log_id):
    entry = db.get_or_404(ActivityLog, log_id)
    data = request.get_json()
    quantity = data.get("quantity")

    try:
        quantity = float(quantity)
    except (ValueError, TypeError):
        return jsonify({"error": "quantity must be a number"}), 400

    if quantity <= 0:
        return jsonify({"error": "quantity must be positive"}), 400

    max_q = MAX_QTY.get(entry.category, 10000)
    if quantity > max_q:
        return jsonify({"error": f"max {max_q} for {entry.category}"}), 400

    entry.quantity = quantity
    entry.co2_kg = round(FACTORS[entry.category][entry.activity] * quantity, 4)
    db.session.commit()

    return jsonify({"message": "updated", "co2_kg": entry.co2_kg}), 200
