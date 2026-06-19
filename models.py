# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ActivityLog(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    date        = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    category    = db.Column(db.String(50), nullable=False)   # transport/food/energy/shopping
    activity    = db.Column(db.String(100), nullable=False)  # car_km, beef_meal, etc.
    quantity    = db.Column(db.Float, nullable=False)
    co2_kg      = db.Column(db.Float, nullable=False)        # pre-calculated at write time
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
