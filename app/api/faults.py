from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.fault import Fault
from app.schemas.fault import FaultCreate, FaultResponse

router = APIRouter(
    prefix="/faults",
    tags=["Faults"]
)


@router.post(
    "/",
    response_model=FaultResponse,
    status_code=status.HTTP_201_CREATED
)
def create_fault(
    fault_data: FaultCreate,
    db: Session = Depends(get_db)
):
    fault = Fault(**fault_data.model_dump())

    db.add(fault)
    db.commit()
    db.refresh(fault)

    return fault


@router.get("/", response_model=list[FaultResponse])
def get_faults(db: Session = Depends(get_db)):

    return db.query(Fault).all()