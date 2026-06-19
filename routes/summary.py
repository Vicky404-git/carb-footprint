# routes/summary.py
from flask import Blueprint, request, jsonify
from models import db, ActivityLog
from sqlalchemy import func
from datetime import date, timedelta
from data.emission_factors import FACTORS, UNITS

summary_bp = Blueprint("summary", __name__)

@summary_bp.route("/meta", methods=["GET"])
def get_meta():
    return jsonify({"factors": FACTORS, "units": UNITS}), 200

@summary_bp.route("/logs", methods=["GET"])
def get_logs():
    date_str = request.args.get("date")        # optional ?date=2026-06-19
    
    query = ActivityLog.query
    if date_str:
        try:
            filter_date = date.fromisoformat(date_str)
            query = query.filter(ActivityLog.date == filter_date)
        except ValueError:
            return jsonify({"error": "invalid date format, use YYYY-MM-DD"}), 400

    logs = query.order_by(ActivityLog.created_at.desc()).all()
    
    return jsonify([{
        "id":       l.id,
        "date":     str(l.date),
        "category": l.category,
        "activity": l.activity,
        "quantity": l.quantity,
        "co2_kg":   l.co2_kg,
        "time":     l.created_at.strftime("%H:%M")
    } for l in logs]), 200


@summary_bp.route("/summary/today", methods=["GET"])
def summary_today():
    today = date.today()
    
    rows = db.session.query(
        ActivityLog.category,
        func.sum(ActivityLog.co2_kg).label("total_co2")
    ).filter(
        ActivityLog.date == today
    ).group_by(ActivityLog.category).all()

    breakdown = {row.category: round(row.total_co2, 3) for row in rows}
    total = round(sum(breakdown.values()), 3)
    goal = 8.0

    return jsonify({
        "date":      str(today),
        "total_co2": total,
        "goal_kg":   goal,
        "under_goal": total <= goal,
        "breakdown": breakdown
    }), 200
