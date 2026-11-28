from fastapi import HTTPException, status

ALLOWED = {
    "open": {"assigned", "cancelled"},
    "assigned": {"in_progress", "cancelled"},
    "in_progress": {"closed"},
    "closed": set(),
    #"closed": {"open"},
    "cancelled": set(),
}


def validate_status_transition(current_status: str, new_status: str):

    allowed_statuses = ALLOWED[current_status]

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Cannot change work order status "
                f"from '{current_status}' to '{new_status}'"
            )
        )