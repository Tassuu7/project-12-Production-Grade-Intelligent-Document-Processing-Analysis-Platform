"""Integration tests for authentication REST endpoints."""
def test_login_flow_success(client):
    res = client.post("/api/v1/auth/login", json={
        "username_or_email": "user@test.com",
        "password": "User@12345"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["user"]["role"] == "user"

def test_login_flow_invalid_password(client):
    res = client.post("/api/v1/auth/login", json={
        "username_or_email": "user@test.com",
        "password": "IncorrectPassword"
    })
    assert res.status_code == 400

def test_user_registration(client):
    res = client.post("/api/v1/auth/register", json={
        "email": "newuser@test.com",
        "username": "newuser",
        "full_name": "New User",
        "password": "NewUserPassword@123"
    })
    assert res.status_code == 200
    assert res.json()["username"] == "newuser"
