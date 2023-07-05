import pytest
from conftest import (app, current_superuser, current_user,
                      get_async_session, override_get_async_session)
from fastapi.testclient import TestClient

from app.models.user import User

superuser = User(
    id=1,
    is_active=True,
    is_verified=True,
    is_superuser=True,
)


@pytest.fixture
def superuser_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[current_superuser] = lambda: superuser
    with TestClient(app) as client:
        yield client

'''author = User(
    id=2,
    is_active=True,
    is_verified=True,
    is_superuser=False,
)

auth = User(
    id=2,
    is_active=True,
    is_verified=True,
    is_superuser=False,
)

anon = User(
    id=3,
    is_active=False,
    is_verified=False,
    is_superuser=False,
)


@pytest.fixture
def user_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[current_user] = lambda: user
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[current_user] = lambda: anon
    with TestClient(app) as client:
        yield client'''

