from fastapi import FastAPI

from app import models  # noqa: F401
from app.api import components, faults, work_orders
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GridOps API",
    description="Utility Maintenance Management API",
    version="1.0.0"
)

app.include_router(faults.router)
app.include_router(work_orders.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to GridOps API"
    }

app.include_router(components.router)