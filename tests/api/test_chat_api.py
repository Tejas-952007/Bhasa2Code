"""Comprehensive integration tests for Chat API endpoints."""

import os
import tempfile
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.app.api.deps import get_current_user_id, get_db, get_llm_service
from backend.app.database.engine import get_engine_args, init_db
from backend.app.database.repositories.user_repository import UserRepository
from backend.app.llm.exceptions import OllamaUnavailableError
from backend.app.llm.schemas import LLMResponse
from backend.app.main import app


@pytest.fixture
def chat_test_env():
    """Create isolated SQLite database and mock LLM service."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_api_chat.db")
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
            db = TestingSessionLocal()
            try:
                user_repo = UserRepository(db)
                if not user_repo.get_by_id("default-user"):
                    user_repo.create(id="default-user", name="Default User", commit=True)
                return "default-user"
            finally:
                db.close()

        mock_llm = MagicMock()
        mock_llm.generate.return_value = LLMResponse(
            text=(
                "Here is a simple calculator in Python:\n\n"
                "```python\ndef add(a, b):\n    return a + b\n```\n\n"
                "### Explanation\n- Adds two numbers.\n- Returns result.\n\n"
                "### Example\n`add(2, 3)` gives `5`"
            ),
            model="qwen2.5-coder:3b",
            prompt_tokens=50,
            completion_tokens=40,
            total_duration_ms=120.0,
        )

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user_id] = override_get_user
        app.dependency_overrides[get_llm_service] = lambda: mock_llm

        client = TestClient(app)
        try:
            yield client, mock_llm, TestingSessionLocal
        finally:
            app.dependency_overrides.clear()
            engine.dispose()


def test_chat_new_session_flow(chat_test_env):
    client, mock_llm, _ = chat_test_env

    resp = client.post(
        "/api/v1/chat",
        json={"message": "python madhe calculator bana", "study_mode": False},
    )
    assert resp.status_code == 200
    data = resp.json()

    assert "session_id" in data
    assert "message_id" in data
    assert data["user_message"]["content"] == "python madhe calculator bana"
    assert data["assistant_message"]["content"]
    assert "explanation" in data["assistant_message"]
    assert len(data["code"]) > 0
    assert data["code"][0]["language"] == "python"
    assert "def add" in data["code"][0]["content"]
    assert data["code"][0]["validation_status"] == "VALID"
    assert data["nlp"]["language"] in ["MARATHI_ENGLISH", "MARATHI", "ENGLISH", "HINGLISH"]


def test_chat_study_mode(chat_test_env):
    client, mock_llm, _ = chat_test_env

    mock_llm.generate.return_value = LLMResponse(
        text=(
            "### Problem Understanding\nUnderstand calculator arithmetic.\n\n"
            "### Algorithm\n1. Take two inputs\n2. Perform operation\n3. Return result\n\n"
            "### Flowchart\nStart -> Input -> Process -> Output -> End\n\n"
            "```python\ndef add(a, b):\n    return a + b\n```\n\n"
            "### Important Points\n- Check division by zero.\n\n"
            "### Viva Questions\nQ: What is a function?\nA: Reusable code block."
        ),
        model="qwen2.5-coder:3b",
        prompt_tokens=100,
        completion_tokens=80,
        total_duration_ms=200.0,
    )

    resp = client.post(
        "/api/v1/chat",
        json={"message": "calculator bana", "study_mode": True},
    )
    assert resp.status_code == 200
    data = resp.json()

    assert data["study"] is not None
    assert "Problem Understanding" in data["study"]["problem_understanding"] or data["study"]["problem_understanding"]
    assert len(data["study"]["algorithm"]) >= 2
    assert "Start -> Input" in data["study"]["flowchart"]
    assert len(data["study"]["viva_questions"]) >= 1


def test_chat_follow_up_existing_session(chat_test_env):
    client, mock_llm, _ = chat_test_env

    # Turn 1
    resp1 = client.post(
        "/api/v1/chat",
        json={"message": "python madhe calculator bana", "study_mode": False},
    )
    session_id = resp1.json()["session_id"]

    # Turn 2
    resp2 = client.post(
        "/api/v1/chat",
        json={
            "session_id": session_id,
            "message": "yat error handling add kar",
            "study_mode": False,
        },
    )
    assert resp2.status_code == 200
    assert resp2.json()["session_id"] == session_id

    # Verify session detail has both user turns
    sess_detail = client.get(f"/api/v1/sessions/{session_id}").json()
    assert len(sess_detail["messages"]) >= 4  # 2 user + 2 assistant


def test_chat_ollama_unavailable(chat_test_env):
    client, mock_llm, _ = chat_test_env
    mock_llm.generate.side_effect = OllamaUnavailableError()

    resp = client.post(
        "/api/v1/chat",
        json={"message": "python madhe calculator bana"},
    )
    assert resp.status_code == 503
    data = resp.json()
    assert data["error"]["code"] == "OLLAMA_UNAVAILABLE"
    assert "The local model could not respond" in data["error"]["message"]


def test_chat_empty_message(chat_test_env):
    client, _, _ = chat_test_env
    resp = client.post(
        "/api/v1/chat",
        json={"message": "   "},
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "BAD_REQUEST"
