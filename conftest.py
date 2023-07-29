import pytest
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app as main_app
from testdbconfig import TestingSessionLocal, engine


@pytest.fixture(scope="function")
def test_app():
    Base.metadata.create_all(bind=engine)  # Create the tables.
    yield main_app
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_app):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def override_dependencies(test_app, db_session):
    test_app.dependency_overrides[get_db] = override_get_db
    yield
    del test_app.dependency_overrides[get_db]


@pytest.fixture(scope="function")
def client(override_dependencies):
    with TestClient(main_app) as client:
        yield client
