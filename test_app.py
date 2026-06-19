import os
# Force the app to use an in-memory DB before it even imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from datetime import date
from app import app
from models import db, ActivityLog

@pytest.fixture
def client():
    app.config["TESTING"] = True
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            # Tear down the database after the test runs
            db.session.remove()
            db.drop_all()

# --- 1. META ENDPOINT TESTS ---

def test_meta_endpoint(client):
    """Ensure the API successfully returns the emission factors."""
    response = client.get("/api/meta")
    assert response.status_code == 200
    assert b"factors" in response.data
    assert b"units" in response.data


# --- 2. LOG CREATION TESTS ---

def test_log_activity_success(client):
    """Test successful creation of a log and verify the CO2 math."""
    payload = {
        "category": "transport",
        "activity": "car",
        "quantity": 100.0  # 100 km
    }
    response = client.post("/api/log", json=payload)
    data = response.get_json()
    
    assert response.status_code == 201
    assert data["message"] == "logged"
    # car factor is 0.00021. 100 * 0.00021 = 0.021
    assert data["co2_kg"] == 0.021
    assert data["category"] == "transport"

def test_log_activity_missing_fields(client):
    """Test logging fails when required fields are missing."""
    response = client.post("/api/log", json={"category": "transport"})
    assert response.status_code == 400
    assert b"required" in response.data

def test_log_activity_invalid_category(client):
    """Test logging fails with a non-existent category."""
    payload = {"category": "spacecraft", "activity": "rocket", "quantity": 1}
    response = client.post("/api/log", json=payload)
    assert response.status_code == 400
    assert b"unknown category" in response.data

def test_log_activity_negative_quantity(client):
    """Test logging fails with negative quantities."""
    payload = {"category": "energy", "activity": "ac", "quantity": -5}
    response = client.post("/api/log", json=payload)
    assert response.status_code == 400
    assert b"positive" in response.data

def test_log_activity_exceeds_max(client):
    """Test validation against MAX_QTY limit."""
    payload = {"category": "food", "activity": "rice", "quantity": 15000} # Max is 10000
    response = client.post("/api/log", json=payload)
    assert response.status_code == 400
    assert b"quantity too high" in response.data


# --- 3. LOG MODIFICATION TESTS ---

def test_delete_log(client):
    """Test successfully deleting an existing log."""
    post_res = client.post("/api/log", json={"category": "shopping", "activity": "plastic_bag", "quantity": 5})
    log_id = post_res.get_json()["id"]
    
    del_res = client.delete(f"/api/log/{log_id}")
    assert del_res.status_code == 200
    
    with app.app_context():
        # Updated to fix SQLAlchemy 2.0 warning
        log = db.session.get(ActivityLog, log_id)
        assert log is None

def test_edit_log(client):
    """Test successfully editing an existing log's quantity and recalculating CO2."""
    post_res = client.post("/api/log", json={"category": "shopping", "activity": "plastic_bag", "quantity": 5})
    log_id = post_res.get_json()["id"]
    
    put_res = client.put(f"/api/log/{log_id}", json={"quantity": 10})
    put_data = put_res.get_json()
    
    assert put_res.status_code == 200
    assert put_data["co2_kg"] == 0.12

# --- 4. DATA RETRIEVAL TESTS ---

def test_get_logs_today(client):
    """Test retrieving logs for a specific date."""
    client.post("/api/log", json={"category": "food", "activity": "dal", "quantity": 200})
    
    today_str = str(date.today())
    response = client.get(f"/api/logs?date={today_str}")
    data = response.get_json()
    
    assert response.status_code == 200
    assert len(data) > 0
    assert data[0]["activity"] == "dal"

def test_summary_today(client):
    """Test the daily breakdown and total calculation."""
    # Add multiple logs
    client.post("/api/log", json={"category": "food", "activity": "rice", "quantity": 100}) # 100 * 0.0028 = 0.28
    client.post("/api/log", json={"category": "energy", "activity": "ac", "quantity": 2})    # 2 * 0.6 = 1.2
    
    response = client.get("/api/summary/today")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["total_co2"] == 1.48
    assert data["breakdown"]["food"] == 0.28
    assert data["breakdown"]["energy"] == 1.20
    assert data["under_goal"] is True  # 1.48 <= 8.0
