# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class ActivityLog(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    date        = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc).date())
    category    = db.Column(db.String(50), nullable=False)   
    activity    = db.Column(db.String(100), nullable=False)  
    quantity    = db.Column(db.Float, nullable=False)
    co2_kg      = db.Column(db.Float, nullable=False)        
    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
