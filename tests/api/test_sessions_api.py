"""Comprehensive integration tests for Sessions API endpoints."""

import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.app.api.deps import get_current_user_id, get_db
from backend.app.database.engine import get_engine_args, init_db
from backend.app.database.repositories.user_repository import UserRepository
from backend.app.main import app


@pytest.fixture
def api_test_client():
    """Create test client with clean SQLite database and dependency overrides."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_api_sessions.db")
        db_url = f"sqlite:///{db_path}"
        engine = create_engine(db_url, **get_engine_args(db_url))

        with engine.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys=ON;"))

        init_db(target_engine=engine, url=db_url)
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        def override_get_db():
            db = TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()

        def override_get_user():
            # Seed default user
            db = TestingSessionLocal()
            try:
                user_repo = UserRepository(db)
                if not user_repo.get_by_id("default-user"):
                    user_repo.create(id="default-user", name="Default User", commit=True)
                return "default-user"
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user_id] = override_get_user

        client = TestClient(app)
        try:
            yield client, TestingSessionLocal
        finally:
            app.dependency_overrides.clear()
            engine.dispose()


def test_create_session(api_test_client):
    client, _ = api_test_client
    resp = client.post("/api/v1/sessions", json={"title": "Python Calculator"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Python Calculator"
    assert "id" in data
    assert data["status"] == "active"


def test_create_session_default_title(api_test_client):
    client, _ = api_test_client
    resp = client.post("/api/v1/sessions", json={})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Untitled Chat"


def test_list_sessions(api_test_client):
    client, _ = api_test_client
    client.post("/api/v1/sessions", json={"title": "Session 1"})
    client.post("/api/v1/sessions", json={"title": "Session 2"})

    resp = client.get("/api/v1/sessions")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 2
    titles = [s["title"] for s in data]
    assert "Session 1" in titles
    assert "Session 2" in titles


def test_get_session_by_id(api_test_client):
    client, _ = api_test_client
    created = client.post("/api/v1/sessions", json={"title": "DBMS Normalization"}).json()
    session_id = created["id"]

    resp = client.get(f"/api/v1/sessions/{session_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == session_id
    assert data["title"] == "DBMS Normalization"
    assert "messages" in data
    assert isinstance(data["messages"], list)


def test_get_session_not_found(api_test_client):
    client, _ = api_test_client
    resp = client.get("/api/v1/sessions/non-existent-id")
    assert resp.status_code == 404
    data = resp.json()
    assert data["error"]["code"] == "SESSION_NOT_FOUND"


def test_update_session_title(api_test_client):
    client, _ = api_test_client
    created = client.post("/api/v1/sessions", json={"title": "Old Title"}).json()
    session_id = created["id"]

    resp = client.patch(f"/api/v1/sessions/{session_id}", json={"title": "New Title"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "New Title"

    # Verify persisted
    get_resp = client.get(f"/api/v1/sessions/{session_id}").json()
    assert get_resp["title"] == "New Title"


def test_delete_session(api_test_client):
    client, _ = api_test_client
    created = client.post("/api/v1/sessions", json={"title": "To Delete"}).json()
    session_id = created["id"]

    del_resp = client.delete(f"/api/v1/sessions/{session_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["ok"] is True

    # Subsequent get should 404
    get_resp = client.get(f"/api/v1/sessions/{session_id}")
    assert get_resp.status_code == 404


def test_ownership_isolation(api_test_client):
    client, TestingSessionLocal = api_test_client

    # Create session as another user in DB
    db = TestingSessionLocal()
    from backend.app.database.repositories.user_repository import UserRepository
    from backend.app.database.repositories.session_repository import SessionRepository
    user_repo = UserRepository(db)
    user_repo.create(id="other-user", name="Other User", commit=True)
    session_repo = SessionRepository(db)
    other_session = session_repo.create(user_id="other-user", title="Other Secret", commit=True)
    other_id = other_session.id
    db.close()

    # Client is authenticated as default-user; accessing other session should be forbidden
    resp = client.get(f"/api/v1/sessions/{other_id}")
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "UNAUTHORIZED_SESSION"
