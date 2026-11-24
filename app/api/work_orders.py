from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.component import Component, WorkOrderPart
from app.schemas.work_order import PartCreate

from app.database import get_db
from app.models.fault import Fault
from app.models.work_order import WorkOrder
from app.schemas.work_order import (
    WorkOrderCreate,
    WorkOrderResponse,
    StatusUpdate
)

from app.models.component import Component, WorkOrderPart
from app.schemas.work_order import PartCreate

from app.services.work_order_service import (
    validate_status_transition
)


router = APIRouter(
    prefix="/work-orders",
    tags=["Work Orders"]
)


@router.post(
    "/",
    response_model=WorkOrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_work_order(
    order_data: WorkOrderCreate,
    db: Session = Depends(get_db)
):

    fault = db.get(Fault, order_data.fault_id)

    if fault is None:
        raise HTTPException(
            status_code=404,
            detail="Fault not found"
        )

    order = WorkOrder(
        fault_id=order_data.fault_id,
        assigned_to=order_data.assigned_to,
        status="open"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order

# @router.post("/{order_id}/parts")
# def add_part_to_work_order(
#     order_id: int,
#     part_data: PartCreate,
#     db: Session = Depends(get_db)
# ):

#     # 1. Check if work order exists
#     order = db.get(WorkOrder, order_id)

#     if order is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Work order not found"
#         )

#     # 2. Check if component exists
#     component = db.get(Component, part_data.component_id)

#     if component is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Component not found"
#         )

#     # 3. Create work order part
#     new_part = WorkOrderPart(
#         work_order_id=order_id,
#         component_id=part_data.component_id,
#         quantity=part_data.quantity
#     )

#     db.add(new_part)
#     db.commit()
#     db.refresh(new_part)

#     return {
#         "id": new_part.id,
#         "work_order_id": new_part.work_order_id,
#         "component_id": new_part.component_id,
#         "quantity": new_part.quantity
#     }


@router.patch(
    "/{order_id}/status",
    response_model=WorkOrderResponse
)
def update_work_order_status(
    order_id: int,
    status_data: StatusUpdate,
    db: Session = Depends(get_db)
):

    order = db.get(WorkOrder, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Work order not found"
        )

    validate_status_transition(
        order.status,
        status_data.status
    )

    order.status = status_data.status

    db.commit()
    db.refresh(order)

    return order


@router.get("/", response_model=list[WorkOrderResponse])
def get_work_orders(
    status_filter: str | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(WorkOrder)

    if status_filter:
        query = query.filter(
            WorkOrder.status == status_filter
        )

    return query.all()


@router.get("/{order_id}", response_model=WorkOrderResponse)
def get_work_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.get(WorkOrder, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Work order not found"
        )

    return order

@router.post("/{order_id}/parts", status_code=201)
def add_part_to_work_order(
    order_id: int,
    part_data: PartCreate,
    db: Session = Depends(get_db)
):

    order = db.get(WorkOrder, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Work order not found"
        )

    if order.status in {"closed", "cancelled"}:
        raise HTTPException(
            status_code=409,
            detail="Cannot modify parts of a closed or cancelled order"
        )

    component = db.get(Component, part_data.component_id)

    if component is None:
        raise HTTPException(
            status_code=404,
            detail="Component not found"
        )

    part = WorkOrderPart(
        work_order_id=order_id,
        component_id=part_data.component_id,
        quantity=part_data.quantity
    )

    db.add(part)
    db.commit()
    db.refresh(part)

    return {
        "id": part.id,
        "work_order_id": part.work_order_id,
        "component_id": part.component_id,
        "quantity": part.quantity
    }