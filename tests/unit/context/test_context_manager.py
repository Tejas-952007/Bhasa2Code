"""Comprehensive unit and integration tests for Bhasha2Code Context Manager (T15)."""

import os
import tempfile
import time
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.app.context import (
    ContextCode,
    ContextError,
    ContextManager,
    ContextMessage,
    ContextPackage,
    ContextPolicy,
    SessionNotFoundError,
    UnauthorizedSessionError,
    is_follow_up,
)
from backend.app.database.engine import get_engine_args, init_db
from backend.app.database.repositories import (
    GeneratedCodeRepository,
    MessageRepository,
    SessionRepository,
    UserRepository,
)
from backend.app.nlp.pipeline import NLPPipeline, get_nlp_pipeline


@pytest.fixture
def test_db_session():
    """Create an isolated temporary SQLite database and yield an active session."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_context.db")
        db_url = f"sqlite:///{db_path}"
        test_engine = create_engine(db_url, **get_engine_args(db_url))

        with test_engine.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys=ON;"))

        init_db(target_engine=test_engine, url=db_url)
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
            test_engine.dispose()


@pytest.fixture
def repos(test_db_session):
    """Provide repository instances."""
    return {
        "user": UserRepository(test_db_session),
        "session": SessionRepository(test_db_session),
        "message": MessageRepository(test_db_session),
        "code": GeneratedCodeRepository(test_db_session),
    }


@pytest.fixture
def context_manager(repos):
    """Provide a ContextManager instance initialized with repositories."""
    return ContextManager(
        session_repository=repos["session"],
        message_repository=repos["message"],
        generated_code_repository=repos["code"],
    )


@pytest.fixture
def test_user(repos):
    """Create a default test user."""
    return repos["user"].create(name="Aditi Deshmukh")


# ---------------------------------------------------------------------------
# 1. Follow-Up Detection Heuristic Tests
# ---------------------------------------------------------------------------

def test_is_follow_up_affirmative_cases():
    """Verify follow-up heuristic correctly flags conversational continuation."""
    follow_up_inputs = [
        "add error handling",
        "make it shorter",
        "optimize this",
        "explain this",
        "convert it to C++",
        "remove comments",
        "add validation",
        "what about edge cases?",
        "yat error handling add kar",
        "tyat logging lava",
        "isko fast banao",
        "same for C++",
        "fix this",
        "यामध्ये validation ॲड कर",
        "step by step explain kar",
        "how about unit tests?",
    ]
    for inp in follow_up_inputs:
        assert is_follow_up(inp) is True, f"Failed to detect follow-up for: {inp}"


def test_is_follow_up_standalone_cases():
    """Verify follow-up heuristic identifies new standalone coding topics."""
    standalone_inputs = [
        "write a Python calculator",
        "what is polymorphism?",
        "create a REST API using FastAPI",
        "python madhe calculator bana",
        "बाइनरी सर्च अल्गोरिदम लिहा",
        "implement a web scraper in Python",
        "what is recursion?",
    ]
    for inp in standalone_inputs:
        assert is_follow_up(inp) is False, f"Erroneously flagged standalone query as follow-up: {inp}"


# ---------------------------------------------------------------------------
# 2. New / Empty Session Tests
# ---------------------------------------------------------------------------

def test_new_session_empty_history(context_manager, repos, test_user):
    """Verify context package generation on an empty session."""
    session = repos["session"].create(user_id=test_user.id, title="Empty Start")

    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message="Hello, can you help me?",
    )

    assert isinstance(package, ContextPackage)
    assert package.session_id == session.id
    assert package.current_message == "Hello, can you help me?"
    assert package.messages == []
    assert package.generated_code == []
    assert package.total_messages == 0
    assert package.truncated is False
    assert package.has_history is False
    assert package.has_code is False
    assert package.session_metadata["title"] == "Empty Start"


# ---------------------------------------------------------------------------
# 3. Critical Multi-Turn Acceptance Case (Calculator -> Error Handling)
# ---------------------------------------------------------------------------

def test_critical_acceptance_calculator_follow_up(context_manager, repos, test_user):
    """Test the primary acceptance case:
    Turn 1: User asks for calculator in Marathi/English
    Turn 2: Assistant provides calculator code
    Turn 3: User asks 'yat error handling add kar'
    Verify previous conversation and generated calculator code are linked.
    """
    session = repos["session"].create(
        user_id=test_user.id,
        title="Calculator Project",
        programming_language="python",
    )

    # Turn 1: User
    msg_turn1 = repos["message"].create(
        session_id=session.id,
        role="user",
        content="python madhe calculator bana",
        detected_language="MARATHI_ENGLISH",
        intent="GENERATE_CODE",
    )

    # Turn 2: Assistant
    calc_code_snippet = (
        "def add(a, b):\n    return a + b\n\n"
        "def subtract(a, b):\n    return a - b\n"
    )
    msg_turn2 = repos["message"].create(
        session_id=session.id,
        role="assistant",
        content="हा Python calculator चा code:\n```python\n" + calc_code_snippet + "```",
    )
    code_artifact = repos["code"].create(
        session_id=session.id,
        message_id=msg_turn2.id,
        language="python",
        code=calc_code_snippet,
        validation_status="valid",
    )

    # Turn 3: User asks for follow-up modification
    turn3_prompt = "yat error handling add kar"

    nlp_pipeline = get_nlp_pipeline()
    nlp_result = nlp_pipeline.analyze(turn3_prompt)

    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message=turn3_prompt,
        nlp_result=nlp_result,
    )

    assert package.session_id == session.id
    assert package.current_message == turn3_prompt
    assert package.total_messages == 2
    assert len(package.messages) == 2

    # Chronological ordering check
    assert package.messages[0].message_id == msg_turn1.id
    assert package.messages[0].role == "user"
    assert "calculator bana" in package.messages[0].content

    assert package.messages[1].message_id == msg_turn2.id
    assert package.messages[1].role == "assistant"

    # Generated code verification
    assert len(package.generated_code) == 1
    assert package.generated_code[0].generated_code_id == code_artifact.id
    assert package.generated_code[0].message_id == msg_turn2.id
    assert "def add(a, b):" in package.generated_code[0].code
    assert package.generated_code[0].validation_status == "valid"

    # Metadata verification
    assert package.metadata is not None
    assert package.metadata.is_follow_up is True
    assert package.metadata.language is not None
    assert package.truncated is False


# ---------------------------------------------------------------------------
# 4. Strict Ownership Isolation Tests
# ---------------------------------------------------------------------------

def test_session_ownership_isolation(context_manager, repos):
    """Verify cross-user session access raises UnauthorizedSessionError without leaking data."""
    user_a = repos["user"].create(name="User Alice")
    user_b = repos["user"].create(name="User Bob")

    session_a = repos["session"].create(user_id=user_a.id, title="Alice Private Session")
    msg_a = repos["message"].create(
        session_id=session_a.id,
        role="user",
        content="Secret message from Alice",
    )
    repos["code"].create(
        session_id=session_a.id,
        message_id=msg_a.id,
        code="secret_key = '12345'",
    )

    # Bob attempts to access Alice's session
    with pytest.raises(UnauthorizedSessionError) as exc_info:
        context_manager.build_context(
            user_id=user_b.id,
            session_id=session_a.id,
            current_message="Can I see your code?",
        )

    assert "not authorized" in str(exc_info.value)


def test_session_not_found(context_manager, test_user):
    """Verify non-existent session ID raises SessionNotFoundError."""
    with pytest.raises(SessionNotFoundError) as exc_info:
        context_manager.build_context(
            user_id=test_user.id,
            session_id="non-existent-session-uuid",
            current_message="Hello?",
        )

    assert "not found" in str(exc_info.value)


# ---------------------------------------------------------------------------
# 5. Chronological Ordering Tests
# ---------------------------------------------------------------------------

def test_chronological_message_ordering(context_manager, repos, test_user):
    """Verify messages in ContextPackage are strictly ordered by created_at ascending."""
    session = repos["session"].create(user_id=test_user.id, title="Order Check")

    msg_ids = []
    for i in range(5):
        msg = repos["message"].create(
            session_id=session.id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"Message step {i}",
        )
        msg_ids.append(msg.id)

    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message="Step 5 next",
    )

    assert len(package.messages) == 5
    for idx, m in enumerate(package.messages):
        assert m.message_id == msg_ids[idx]
        assert m.content == f"Message step {idx}"


# ---------------------------------------------------------------------------
# 6. Standalone Query Context Budgeting
# ---------------------------------------------------------------------------

def test_standalone_query_budget(context_manager, repos, test_user):
    """Verify standalone questions pull limited recent context rather than full budget."""
    session = repos["session"].create(user_id=test_user.id, title="Topic Switch")

    # Add 10 conversational turns
    for i in range(10):
        repos["message"].create(
            session_id=session.id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"History message {i}",
        )

    policy = ContextPolicy(max_messages=8, standalone_max_messages=3)

    # Standalone query
    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message="what is polymorphism in Python?",
        policy=policy,
    )

    assert package.metadata.is_follow_up is False
    # Standalone query pulls at most standalone_max_messages
    assert len(package.messages) == 3
    assert package.messages[-1].content == "History message 9"


# ---------------------------------------------------------------------------
# 7. Current Code Extraction Tests
# ---------------------------------------------------------------------------

def test_current_code_preservation(context_manager, repos, test_user):
    """Verify current message code segment is extracted and preserved in ContextPackage."""
    session = repos["session"].create(user_id=test_user.id, title="Code Input Test")

    code_snippet = "def buggy_function(x):\n    return x / 0"
    user_prompt = f"fix this code:\n```python\n{code_snippet}\n```"

    nlp_pipeline = get_nlp_pipeline()
    nlp_result = nlp_pipeline.analyze(user_prompt)

    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message=user_prompt,
        nlp_result=nlp_result,
    )

    assert package.current_code is not None
    assert "return x / 0" in package.current_code
    assert package.has_code is True


def test_traceback_input_preservation(context_manager, repos, test_user):
    """Verify user message with stack trace preserves error context in current_code."""
    session = repos["session"].create(user_id=test_user.id, title="Traceback Test")

    traceback_text = (
        "Traceback (most recent call last):\n"
        '  File "main.py", line 12, in <module>\n'
        "ZeroDivisionError: division by zero"
    )
    user_prompt = f"error yet ahe bagha:\n{traceback_text}"

    nlp_pipeline = get_nlp_pipeline()
    nlp_result = nlp_pipeline.analyze(user_prompt)

    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message=user_prompt,
        nlp_result=nlp_result,
    )

    assert package.current_code is not None
    assert "ZeroDivisionError" in package.current_code


# ---------------------------------------------------------------------------
# 8. Context Window Truncation Tests
# ---------------------------------------------------------------------------

def test_truncation_max_messages(context_manager, repos, test_user):
    """Verify oldest messages are dropped and truncated flag is set when exceeding max_messages."""
    session = repos["session"].create(user_id=test_user.id, title="Long Session")

    for i in range(15):
        repos["message"].create(
            session_id=session.id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"Turn message {i}",
        )

    policy = ContextPolicy(max_messages=5)
    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message="optimize this",
        policy=policy,
    )

    assert len(package.messages) == 5
    assert package.messages[0].content == "Turn message 10"
    assert package.messages[-1].content == "Turn message 14"
    assert package.truncated is True
    assert package.total_messages == 15


def test_truncation_max_characters(context_manager, repos, test_user):
    """Verify messages exceeding character budget are dropped oldest-first."""
    session = repos["session"].create(user_id=test_user.id, title="Heavy Char Session")

    repos["message"].create(
        session_id=session.id,
        role="user",
        content="A" * 500,
    )
    repos["message"].create(
        session_id=session.id,
        role="assistant",
        content="B" * 500,
    )
    repos["message"].create(
        session_id=session.id,
        role="user",
        content="C" * 200,
    )

    # Budget allows ~800 chars total (500 + 500 + 200 = 1200 -> drops oldest 500 -> 700 <= 800)
    policy = ContextPolicy(max_messages=10, max_characters=800)
    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message="explain this",
        policy=policy,
    )

    assert package.truncated is True
    # The oldest 500 char message should have been dropped
    assert len(package.messages) == 2
    assert "B" * 500 in package.messages[0].content
    assert "C" * 200 in package.messages[1].content


def test_truncation_generated_code_budget(context_manager, repos, test_user):
    """Verify generated code truncation drops older items and truncates oversized code."""
    session = repos["session"].create(user_id=test_user.id, title="Heavy Code Session")

    msg_1 = repos["message"].create(session_id=session.id, role="user", content="msg 1")
    repos["code"].create(
        session_id=session.id,
        message_id=msg_1.id,
        code="# Code artifact 1\n" + "x = 1\n" * 50,
    )
    msg_2 = repos["message"].create(session_id=session.id, role="assistant", content="msg 2")
    repos["code"].create(
        session_id=session.id,
        message_id=msg_2.id,
        code="# Code artifact 2\n" + "y = 2\n" * 50,
    )

    policy = ContextPolicy(max_generated_code_items=1, max_code_characters=100)
    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message="make it faster",
        policy=policy,
    )

    assert package.truncated is True
    assert len(package.generated_code) == 1
    assert "truncated to fit context budget" in package.generated_code[0].code


# ---------------------------------------------------------------------------
# 9. Determinism Tests
# ---------------------------------------------------------------------------

def test_context_manager_determinism(context_manager, repos, test_user):
    """Verify repeated executions produce strictly identical ContextPackage outputs."""
    session = repos["session"].create(user_id=test_user.id, title="Deterministic Test")

    for i in range(4):
        msg = repos["message"].create(
            session_id=session.id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"Message {i}",
        )
        if i == 1:
            repos["code"].create(
                session_id=session.id,
                message_id=msg.id,
                code="print('Hello World')",
            )

    packages = []
    for _ in range(5):
        pkg = context_manager.build_context(
            user_id=test_user.id,
            session_id=session.id,
            current_message="yat error handling add kar",
        )
        packages.append(pkg.model_dump())

    # All runs must produce identical dictionary outputs
    for i in range(1, len(packages)):
        assert packages[i] == packages[0], f"Run {i} differed from run 0!"


# ---------------------------------------------------------------------------
# 10. Input Validation & Error Handling Tests
# ---------------------------------------------------------------------------

def test_missing_parameters_validation(context_manager, test_user):
    """Verify missing required parameters raise ValueError."""
    with pytest.raises(ValueError, match="user_id is required"):
        context_manager.build_context(
            user_id="",
            session_id="dummy-session",
            current_message="hello",
        )

    with pytest.raises(ValueError, match="session_id is required"):
        context_manager.build_context(
            user_id=test_user.id,
            session_id="",
            current_message="hello",
        )

    with pytest.raises(ValueError, match="current_message is required"):
        context_manager.build_context(
            user_id=test_user.id,
            session_id="dummy-session",
            current_message=None,
        )


def test_empty_string_message_handled(context_manager, repos, test_user):
    """Verify empty string current message is safely handled without error."""
    session = repos["session"].create(user_id=test_user.id, title="Empty Input")

    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message="",
    )

    assert package.current_message == ""
    assert package.session_id == session.id


# ---------------------------------------------------------------------------
# 11. Performance Sanity Benchmark
# ---------------------------------------------------------------------------

def test_performance_sanity_benchmark(context_manager, repos, test_user):
    """Benchmark basic context build latency to ensure fast O(1) database queries."""
    session = repos["session"].create(user_id=test_user.id, title="Perf Session")

    for i in range(10):
        msg = repos["message"].create(
            session_id=session.id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"Quick msg {i}",
        )
        if i % 3 == 0:
            repos["code"].create(
                session_id=session.id,
                message_id=msg.id,
                code="x = 10",
            )

    start = time.perf_counter()
    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message="optimize it",
    )
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert package is not None
    # Building context should execute well within 50ms on local SQLite
    assert elapsed_ms < 50.0, f"Context build took {elapsed_ms:.2f} ms, expected < 50 ms"


# ---------------------------------------------------------------------------
# 12. Additional Edge Cases & Robustness
# ---------------------------------------------------------------------------

def test_session_current_code_fallback(context_manager, repos, test_user):
    """Verify session.current_code is used if current message does not contain code snippets."""
    session = repos["session"].create(
        user_id=test_user.id,
        title="Session Code Fallback",
        current_code="total = sum([1, 2, 3])",
    )

    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message="explain this code",
    )

    assert package.current_code == "total = sum([1, 2, 3])"
    assert package.has_code is True


def test_database_failure_propagation(context_manager, test_user, monkeypatch):
    """Verify underlying repository/database exceptions are cleanly propagated, not swallowed."""
    def broken_get_by_id(*args, **kwargs):
        raise RuntimeError("Simulated database connection failure")

    monkeypatch.setattr(context_manager.session_repo, "get_by_id", broken_get_by_id)

    with pytest.raises(RuntimeError, match="Simulated database connection failure"):
        context_manager.build_context(
            user_id=test_user.id,
            session_id="some-id",
            current_message="hello",
        )


def test_context_package_dict_access(context_manager, repos, test_user):
    """Verify ContextPackage supports dictionary subscripting and serialization."""
    session = repos["session"].create(user_id=test_user.id, title="Dict Access")

    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message="write code",
    )

    assert package["session_id"] == session.id
    assert package["current_message"] == "write code"
    d = package.to_dict()
    assert isinstance(d, dict)
    assert d["session_id"] == session.id


def test_multiple_code_artifacts_recency_ordering(context_manager, repos, test_user):
    """Verify that when multiple code artifacts exist, newest first retrieval order is maintained."""
    session = repos["session"].create(user_id=test_user.id, title="Multi-Code Ordering")

    msg1 = repos["message"].create(session_id=session.id, role="assistant", content="Version 1")
    code1 = repos["code"].create(
        session_id=session.id,
        message_id=msg1.id,
        code="# Version 1 Code",
    )

    msg2 = repos["message"].create(session_id=session.id, role="assistant", content="Version 2")
    code2 = repos["code"].create(
        session_id=session.id,
        message_id=msg2.id,
        code="# Version 2 Code",
    )

    package = context_manager.build_context(
        user_id=test_user.id,
        session_id=session.id,
        current_message="make it faster",
    )

    assert len(package.generated_code) == 2
    # Newest artifact should be at index 0
    assert package.generated_code[0].generated_code_id == code2.id
    assert package.generated_code[0].code == "# Version 2 Code"
    assert package.generated_code[1].generated_code_id == code1.id

