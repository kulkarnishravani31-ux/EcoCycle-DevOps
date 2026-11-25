import os
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret"
from app import app, db

def setup_function():
    app.config["TESTING"] = True
    with app.app_context():
        db.drop_all()
        db.create_all()

def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_health_endpoint():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"

def test_register_and_login():
    client = app.test_client()
    response = client.post("/register", data={
        "name": "Test Student", "email": "student@example.com", "password": "StrongPass123"
    }, follow_redirects=True)
    assert response.status_code == 200
    response = client.post("/login", data={
        "email": "student@example.com", "password": "StrongPass123"
    }, follow_redirects=True)
    assert response.status_code == 200
