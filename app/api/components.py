from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.component import Component
from app.schemas.component import ComponentCreate, ComponentResponse

router = APIRouter(
    prefix="/components",
    tags=["Components"]
)


@router.post(
    "/",
    response_model=ComponentResponse,
    status_code=201
)
def create_component(
    data: ComponentCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Component).filter(
        (Component.name == data.name) |
        (Component.code == data.code)
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Component already exists"
        )

    component = Component(**data.model_dump())

    db.add(component)
    db.commit()
    db.refresh(component)

    return component


@router.get("/", response_model=list[ComponentResponse])
def get_components(db: Session = Depends(get_db)):

    return db.query(Component).all()