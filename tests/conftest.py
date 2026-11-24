import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=test_engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db):

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

def create_fault(client):

    response = client.post(
        "/faults/",
        json={
            "description": "Cable failure",
            "location": "Giza",
            "severity": "medium",
            "reported_by": "Technician 10"
        }
    )

    return response.json()["id"]

import pytest

#this line to solve error of testing
@pytest.fixture
def create_fault():

    def _create_fault(client):

        response = client.post(
            "/faults/",
            json={
                "description": "Cable failure",
                "location": "Giza",
                "severity": "medium",
                "reported_by": "Technician 10"
            }
        )

        assert response.status_code == 201, response.text

        return response.json()["id"]

    return _create_fault