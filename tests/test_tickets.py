"""
Ticket endpoint tests.

Tests create and list ticket endpoints with validation.

Author: Project
Last Modified: 2026-02-12
"""


def test_create_ticket_success(client):
    """Test creating a ticket with valid data."""
    payload = {
        "title": "Test ticket",
        "description": "This is a test",
        "priority": "high",
    }

    response = client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Test ticket"
    assert data["data"]["description"] == "This is a test"
    assert data["data"]["priority"] == "high"
    assert data["data"]["status"] == "open"
    assert "id" in data["data"]
    assert "created_at" in data["data"]
    assert data["message"] == "Ticket created successfully"


def test_create_ticket_validation_error(client):
    """Test creating a ticket with invalid data."""
    payload = {
        "title": "",  # Empty title should fail
        "priority": "invalid",  # Invalid priority
    }

    response = client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 422  # Validation error


def test_list_tickets_empty(client):
    """Test listing tickets when none exist."""
    response = client.get("/api/v1/tickets")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["data"] == []
    assert data["message"] == "Retrieved 0 tickets"


def test_list_tickets_with_data(client):
    """Test listing tickets after creating some."""
    # Create tickets
    for i in range(3):
        client.post(
            "/api/v1/tickets",
            json={"title": f"Ticket {i}", "priority": "medium"},
        )

    # List tickets
    response = client.get("/api/v1/tickets")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 3
    assert data["message"] == "Retrieved 3 tickets"


def test_list_tickets_pagination(client):
    """Test ticket pagination."""
    # Create 5 tickets
    for i in range(5):
        client.post(
            "/api/v1/tickets",
            json={"title": f"Ticket {i}", "priority": "low"},
        )

    # Get first 2
    response = client.get("/api/v1/tickets?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2

    # Get next 2
    response = client.get("/api/v1/tickets?limit=2&offset=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
