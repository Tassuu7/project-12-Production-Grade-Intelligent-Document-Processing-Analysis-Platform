import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.core.security import hash_password, create_access_token
from app.models.user import User
from app.main import app

TEST_DB_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    # Seed test users
    admin_user = User(
        id=1,
        email="admin@test.com",
        username="admin",
        full_name="Admin User",
        hashed_password=hash_password("Admin@12345"),
        role="admin",
        is_active=True,
        is_verified=True
    )
    test_user = User(
        id=2,
        email="user@test.com",
        username="user",
        full_name="Standard User",
        hashed_password=hash_password("User@12345"),
        role="user",
        is_active=True,
        is_verified=True
    )
    session.add_all([admin_user, test_user])
    session.commit()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def user_token():
    return create_access_token(2, "user", "user@test.com")

@pytest.fixture
def admin_token():
    return create_access_token(1, "admin", "admin@test.com")
