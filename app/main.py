from fastapi import FastAPI

from app.database import Base, engine
from app import models

from app.api import faults, work_orders
from app.api import components



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