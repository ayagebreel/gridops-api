def test_create_fault(client):

    response = client.post(
        "/faults/",
        json={
            "description": "Transformer failure",
            "location": "Giza Zone 3",
            "severity": "high",
            "reported_by": "Technician 10"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["description"] == "Transformer failure"
    assert data["severity"] == "high"
    assert "id" in data

def test_create_fault_with_invalid_severity(client):

    response = client.post(
        "/faults/",
        json={
            "description": "Transformer failure",
            "location": "Giza",
            "severity": "urgent",
            "reported_by": "Technician 10"
        }
    )

    assert response.status_code == 422