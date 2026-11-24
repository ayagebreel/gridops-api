def test_create_work_order(client,create_fault):

    fault_id = create_fault(client)

    response = client.post(
        "/work-orders/",
        json={
            "fault_id": fault_id,
            "assigned_to": None
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["fault_id"] == fault_id
    assert data["status"] == "open"

def test_create_work_order_with_missing_fault(client):

    response = client.post(
        "/work-orders/",
        json={
            "fault_id": 999,
            "assigned_to": None
        }
    )

    assert response.status_code == 404


def test_valid_status_transition(client ,create_fault):

    fault_id = create_fault(client)

    order_response = client.post(
        "/work-orders/",
        json={
            "fault_id": fault_id
        }
    )

    order_id = order_response.json()["id"]

    response = client.patch(
        f"/work-orders/{order_id}/status",
        json={"status": "assigned"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "assigned"

import pytest


@pytest.mark.parametrize(
    "start,target",
    [
        ("open", "closed"),
        ("closed", "open"),
        ("assigned", "open"),
        ("cancelled", "assigned"),
        ("in_progress", "assigned"),
    ]
)
def test_illegal_moves_return_409(client, create_fault, start, target):

    fault_id = create_fault(client)

    order_response = client.post(
        "/work-orders/",
        json={"fault_id": fault_id}
    )

    order_id = order_response.json()["id"]

    # Move the order to the required starting status.
    if start != "open":
        setup_moves = {
            "assigned": ["assigned"],
            "closed": ["assigned", "in_progress", "closed"],
            "cancelled": ["cancelled"],
            "in_progress": ["assigned", "in_progress"],
        }

        for new_status in setup_moves[start]:
            client.patch(
                f"/work-orders/{order_id}/status",
                json={"status": new_status}
            )

    response = client.patch(
        f"/work-orders/{order_id}/status",
        json={"status": target}
    )

    assert response.status_code == 409

@pytest.mark.parametrize(
    "quantity",
    [0, -1, 101]
)
def test_invalid_component_quantity(client, quantity):

    response = client.post(
        "/work-orders/1/parts",
        json={
            "component_id": 1,
            "quantity": quantity
        }
    )

    assert response.status_code == 422

