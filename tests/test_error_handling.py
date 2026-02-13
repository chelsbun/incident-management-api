"""
Error handling and exception handler tests.

Tests that all exception handlers return proper envelope format
and handle errors safely without exposing internal details.

Author: Project
Last Modified: 2026-02-12
"""
from unittest.mock import patch


def test_validation_error_handling(client):
    """Test HTTPException handler for validation errors."""
    # Invalid payload - empty title
    payload = {"title": "", "priority": "invalid"}
    
    response = client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 422


def test_database_error_handling(client):
    """Test that database errors are caught and rolled back."""
    # This test verifies the try/except in create_ticket
    # We'll mock db.commit to raise an error
    with patch("app.api.tickets.Session.commit") as mock_commit:
        from sqlalchemy.exc import OperationalError
        mock_commit.side_effect = OperationalError("DB connection lost", None, None)
        
        payload = {"title": "Test ticket", "priority": "high"}
        response = client.post("/api/v1/tickets", json=payload)
        
        # Should return 500 due to database error
        assert response.status_code == 500
        
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        # Should not expose internal DB details to client
        assert "OperationalError" not in str(data)
