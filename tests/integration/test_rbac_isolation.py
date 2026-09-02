"""Integration tests for strict RBAC user isolation."""
def test_user_cannot_access_admin_stats(client, user_token):
    res = client.get("/api/v1/admin/stats", headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == 403

def test_admin_can_access_admin_stats(client, admin_token):
    res = client.get("/api/v1/admin/stats", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    data = res.json()
    assert "total_users" in data
    assert "total_documents" in data
