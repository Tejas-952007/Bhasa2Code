"""Comprehensive integration and unit tests for Streaming Chat API endpoint."""

import json
import os
import tempfile
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.app.api.deps import get_current_user_id, get_db, get_llm_service
from backend.app.database.engine import get_engine_args, init_db
from backend.app.database.repositories.message_repository import MessageRepository
from backend.app.database.repositories.user_repository import UserRepository
from backend.app.llm.exceptions import OllamaUnavailableError
from backend.app.main import app


@pytest.fixture
def stream_test_env():
    """Create isolated SQLite database and mock streaming LLM service."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_api_chat_stream.db")
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

        async def default_stream_generator(prompt_spec, options=None):
            yield {"token": "हो, ", "done": False}
            yield {"token": "Python मध्ये calculator:\n\n", "done": False}
            yield {"token": "```python\ndef add(a, b):\n    return a + b\n```\n\n", "done": False}
            yield {"token": "### Explanation\n- Adds two numbers.", "done": True}

        mock_llm.generate_stream.side_effect = default_stream_generator

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user_id] = override_get_user
        app.dependency_overrides[get_llm_service] = lambda: mock_llm

        client = TestClient(app)
        try:
            yield client, mock_llm, TestingSessionLocal
        finally:
            app.dependency_overrides.clear()
            engine.dispose()


def parse_sse_events(response_text: str):
    """Parse raw SSE text into structured events."""
    events = []
    current_event = {}
    for line in response_text.splitlines():
        line = line.strip()
        if not line:
            if current_event:
                events.append(current_event)
                current_event = {}
            continue
        if line.startswith("event:"):
            current_event["event"] = line[len("event:"):].strip()
        elif line.startswith("data:"):
            data_str = line[len("data:"):].strip()
            try:
                current_event["data"] = json.loads(data_str)
            except json.JSONDecodeError:
                current_event["data"] = data_str
    if current_event:
        events.append(current_event)
    return events


def test_stream_event_sequence_and_first_token(stream_test_env):
    """Verify SSE event ordering: start -> token... -> complete."""
    client, mock_llm, _ = stream_test_env

    resp = client.post(
        "/api/v1/chat/stream",
        json={"message": "python madhe calculator bana", "study_mode": False},
    )
    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers["content-type"]

    events = parse_sse_events(resp.text)
    assert len(events) >= 3

    # First event MUST be start
    first = events[0]
    assert first["event"] == "start"
    assert first["data"]["type"] == "start"
    assert "session_id" in first["data"]
    assert "user_message_id" in first["data"]

    # Intermediate events are tokens
    token_events = [e for e in events if e.get("event") == "token"]
    assert len(token_events) > 0
    assert token_events[0]["data"]["token"] == "हो, "

    # Terminal event MUST be complete
    last = events[-1]
    assert last["event"] == "complete"
    assert last["data"]["type"] == "complete"
    assert "assistant_message" in last["data"]
    assert len(last["data"]["code"]) == 1
    assert last["data"]["code"][0]["language"] == "python"
    assert "def add" in last["data"]["code"][0]["content"]
    assert last["data"]["code"][0]["validation_status"] == "VALID"


def test_stream_idempotent_duplicate_prevention(stream_test_env):
    """Verify client_turn_id prevents duplicate message generation."""
    client, mock_llm, SessionLocal = stream_test_env

    turn_id = "test-turn-id-duplicate-check"

    # Turn 1
    resp1 = client.post(
        "/api/v1/chat/stream",
        json={"message": "test duplicate message", "client_turn_id": turn_id},
    )
    assert resp1.status_code == 200
    events1 = parse_sse_events(resp1.text)
    complete1 = [e for e in events1 if e.get("event") == "complete"][0]

    # Turn 2 with identical client_turn_id
    resp2 = client.post(
        "/api/v1/chat/stream",
        json={
            "session_id": complete1["data"]["session_id"],
            "message": "test duplicate message",
            "client_turn_id": turn_id,
        },
    )
    assert resp2.status_code == 200
    events2 = parse_sse_events(resp2.text)
    complete2 = [e for e in events2 if e.get("event") == "complete"][0]

    # Content and assistant message ID match the cached turn
    assert complete2["data"]["assistant_message"]["id"] == complete1["data"]["assistant_message"]["id"]

    # Verify only 1 user message and 1 assistant message in DB for this turn
    with SessionLocal() as db:
        msg_repo = MessageRepository(db)
        msgs = msg_repo.list_by_session(complete1["data"]["session_id"])
        user_msgs = [m for m in msgs if m.role == "user"]
        assert len(user_msgs) == 1
        assert user_msgs[0].content == "test duplicate message"


def test_stream_flowchart_vs_code_separation(stream_test_env):
    """Verify ASCII flowchart is isolated as study.flowchart and NOT treated as python code."""
    client, mock_llm, _ = stream_test_env

    async def flowchart_stream(prompt_spec, options=None):
        yield {"token": "### Flowchart\n", "done": False}
        yield {
            "token": "+-----------+\n|   Start   |\n+-----------+\n      |\n      v\n+-----------+\n| Calculate |\n+-----------+\n      |\n      v\n+-----------+\n|    End    |\n+-----------+\n\n",
            "done": False,
        }
        yield {"token": "### Code\n```python\ndef calculate(a, b):\n    return a * b\n```\n\n", "done": False}
        yield {"token": "### Explanation\nCalculates multiplication.", "done": True}

    mock_llm.generate_stream.side_effect = flowchart_stream

    resp = client.post(
        "/api/v1/chat/stream",
        json={"message": "calculator bana flowchart ani code de", "study_mode": True},
    )
    assert resp.status_code == 200
    events = parse_sse_events(resp.text)
    complete_event = [e for e in events if e.get("event") == "complete"][0]
    data = complete_event["data"]

    # Flowchart is populated in study
    assert data["study"] is not None
    assert "Start" in data["study"]["flowchart"]
    assert "+-----------+" in data["study"]["flowchart"]

    # Exactly ONE code block (calculate function), flowchart is NOT code
    assert len(data["code"]) == 1
    assert data["code"][0]["language"] == "python"
    assert "def calculate" in data["code"][0]["content"]
    assert "+-----------+" not in data["code"][0]["content"]
    assert data["code"][0]["validation_status"] == "VALID"


def test_stream_ollama_unavailable_error(stream_test_env):
    """Verify Ollama error emits structured SSE error event."""
    client, mock_llm, _ = stream_test_env

    async def failing_stream(prompt_spec, options=None):
        raise OllamaUnavailableError("Ollama daemon is offline")
        yield {}

    mock_llm.generate_stream.side_effect = failing_stream

    resp = client.post(
        "/api/v1/chat/stream",
        json={"message": "hello", "study_mode": False},
    )
    assert resp.status_code == 200
    events = parse_sse_events(resp.text)

    error_events = [e for e in events if e.get("event") == "error"]
    assert len(error_events) == 1
    assert error_events[0]["data"]["type"] == "error"
    assert "unavailable" in error_events[0]["data"]["message"].lower() or "offline" in error_events[0]["data"]["message"].lower()
