import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infra.database import metadata
from app.infra.mappers.mapper import start_mappers
import app.infra.database as database


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    engine = create_engine("sqlite:///:memory:")

    start_mappers()
    metadata.create_all(engine)

    TestingSessionLocal = sessionmaker(bind=engine)
    database.SessionLocal = TestingSessionLocal  # override global

    yield


@pytest.fixture
def session():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
