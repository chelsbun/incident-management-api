"""
Health endpoint tests.

Tests API and database health check endpoints.

Author: Project
Last Modified: 2026-02-12
"""


def test_health_check(client):
    """Test API health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "ok"
    assert data["message"] == "API is healthy"
    assert data["error"] is None


def test_db_health_check(client):
    """Test database health check endpoint."""
    response = client.get("/db-health")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["data"]["db"] == "ok"
    assert data["message"] == "Database is healthy"
    assert data["error"] is None
