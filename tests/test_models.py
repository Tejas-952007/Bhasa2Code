import os
import tempfile
import uuid
from datetime import datetime, timezone
import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from backend.app.database.base import Base
from backend.app.database.engine import init_db, get_engine_args
from backend.app.database.models import (
    User,
    Session,
    Message,
    SavedMessage,
    Note,
    GeneratedCode,
    DebugHistory,
)


@pytest.fixture
def isolated_db():
    """Create an isolated temporary SQLite database for model testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_models.db")
        db_url = f"sqlite:///{db_path}"
        test_engine = create_engine(db_url, **get_engine_args(db_url))

        # Enable SQLite foreign key pragma on connection
        with test_engine.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys=ON;"))

        init_db(target_engine=test_engine, url=db_url)
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

        yield {
            "engine": test_engine,
            "session_factory": TestingSessionLocal,
            "path": db_path,
        }

        test_engine.dispose()


def test_all_seven_tables_created(isolated_db):
    """Verify all 7 approved database tables are created."""
    engine = isolated_db["engine"]
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())

    expected_tables = {
        "users",
        "sessions",
        "messages",
        "saved_messages",
        "notes",
        "generated_code",
        "debug_history",
    }
    assert expected_tables.issubset(table_names)


def test_user_creation(isolated_db):
    """Verify User model creation with auto-generated UUID and timestamps."""
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        user = User(name="Alice Developer")
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert len(user.id) == 36
        assert user.name == "Alice Developer"
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)


def test_session_relationship(isolated_db):
    """Verify Session creation linked to User and bidirectional relationship."""
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        user = User(name="Bob")
        session = Session(
            user=user,
            title="Python Palindrome Study",
            current_language="marathi",
            programming_language="python",
            current_code="def is_palindrome(s): return s == s[::-1]",
        )
        db.add_all([user, session])
        db.commit()

        db.refresh(user)
        assert len(user.sessions) == 1
        assert user.sessions[0].title == "Python Palindrome Study"
        assert user.sessions[0].current_language == "marathi"
        assert session.user.id == user.id


def test_message_creation_and_ordering(isolated_db):
    """Verify Message model creation, metadata, and session ordering."""
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        user = User(name="Charlie")
        session = Session(user=user, title="Coding Chat")
        msg1 = Message(
            session=session,
            role="user",
            content="python madhe code dya",
            detected_language="marathi",
            intent="code_generation",
            tone="casual",
            programming_language="python",
        )
        msg2 = Message(
            session=session,
            role="assistant",
            content="Ha code ghya: print('Hello')",
            programming_language="python",
        )
        db.add_all([user, session, msg1, msg2])
        db.commit()

        db.refresh(session)
        assert len(session.messages) == 2
        assert session.messages[0].role == "user"
        assert session.messages[0].detected_language == "marathi"
        assert session.messages[1].role == "assistant"


def test_saved_message_uniqueness(isolated_db):
    """Verify SavedMessage relationship and unique constraint (user_id, message_id)."""
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        user = User(name="David")
        session = Session(user=user, title="Session 1")
        msg = Message(session=session, role="assistant", content="Important note")
        saved = SavedMessage(user=user, message=msg, label="Important")
        db.add_all([user, session, msg, saved])
        db.commit()

        assert len(user.saved_messages) == 1
        assert user.saved_messages[0].label == "Important"

        # Attempt to save the exact same message again for the same user
        duplicate_saved = SavedMessage(user_id=user.id, message_id=msg.id, label="Duplicate")
        db.add(duplicate_saved)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()


def test_note_independence_and_session_link(isolated_db):
    """Verify Note can be standalone or optionally linked to a Session."""
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        user = User(name="Eva")
        session = Session(user=user, title="Session 2")

        # Independent note (session_id=None)
        independent_note = Note(user=user, title="Independent Note", content="My thoughts")
        # Session-linked note
        linked_note = Note(user=user, session=session, title="Session Note", content="Code pointers")

        db.add_all([user, session, independent_note, linked_note])
        db.commit()

        db.refresh(user)
        assert len(user.notes) == 2
        assert independent_note.session_id is None
        assert linked_note.session_id == session.id


def test_generated_code_model(isolated_db):
    """Verify GeneratedCode creation and relationships with Session and Message."""
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        user = User(name="Frank")
        session = Session(user=user, title="Code Gen Session")
        msg = Message(session=session, role="assistant", content="Generated code block")
        code_artifact = GeneratedCode(
            session=session,
            message=msg,
            language="python",
            code="def add(a, b):\n    return a + b\n",
            validation_status="validated",
        )
        db.add_all([user, session, msg, code_artifact])
        db.commit()

        db.refresh(session)
        assert len(session.generated_codes) == 1
        assert session.generated_codes[0].language == "python"
        assert session.generated_codes[0].validation_status == "validated"
        assert len(msg.generated_codes) == 1


def test_debug_history_model(isolated_db):
    """Verify DebugHistory records debugging operations and results."""
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        user = User(name="Grace")
        session = Session(user=user, title="Debug Session")
        debug_entry = DebugHistory(
            session=session,
            original_code="print(x",
            error_message="SyntaxError: '(' was never closed",
            corrected_code="print(x)",
            validation_status="passed",
            attempt_count=1,
        )
        db.add_all([user, session, debug_entry])
        db.commit()

        db.refresh(session)
        assert len(session.debug_histories) == 1
        assert session.debug_histories[0].error_message == "SyntaxError: '(' was never closed"
        assert session.debug_histories[0].validation_status == "passed"


def test_foreign_key_enforcement(isolated_db):
    """Verify SQLite rejects records with invalid foreign keys."""
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        non_existent_id = str(uuid.uuid4())
        orphan_session = Session(user_id=non_existent_id, title="Orphan Session")
        db.add(orphan_session)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()


def test_nullability_constraints(isolated_db):
    """Verify database rejects records missing mandatory non-nullable fields."""
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        user = User(name="Henry")
        session = Session(user=user, title="Test Session")
        db.add_all([user, session])
        db.commit()

        # Missing content in message
        invalid_message = Message(session_id=session.id, role="user", content=None)
        db.add(invalid_message)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()


def test_cascade_deletion(isolated_db):
    """Verify deleting a User or Session cascades to dependent entities appropriately."""
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        user = User(name="Ivy")
        session = Session(user=user, title="Cascade Session")
        msg = Message(session=session, role="user", content="Hello")
        code = GeneratedCode(session=session, message=msg, language="python", code="print(1)")
        debug = DebugHistory(session=session, original_code="err", error_message="err")
        note = Note(user=user, session=session, title="Note", content="Content")
        saved = SavedMessage(user=user, message=msg)

        db.add_all([user, session, msg, code, debug, note, saved])
        db.commit()

        # Delete session
        db.delete(session)
        db.commit()

        # Messages, GeneratedCode, DebugHistory should be deleted
        assert db.query(Message).filter_by(id=msg.id).first() is None
        assert db.query(GeneratedCode).filter_by(id=code.id).first() is None
        assert db.query(DebugHistory).filter_by(id=debug.id).first() is None

        # Note had ON DELETE SET NULL for session_id, so note still exists for user
        db.refresh(note)
        assert note.session_id is None
        assert note.user_id == user.id

        # Delete user
        db.delete(user)
        db.commit()

        # Note and SavedMessage should be deleted
        assert db.query(Note).filter_by(id=note.id).first() is None
        assert db.query(SavedMessage).filter_by(id=saved.id).first() is None


def test_base_metadata_registration():
    """Verify that Base.metadata contains all 7 application tables."""
    expected_tables = {
        "users",
        "sessions",
        "messages",
        "saved_messages",
        "notes",
        "generated_code",
        "debug_history",
    }
    registered_tables = set(Base.metadata.tables.keys())
    assert expected_tables.issubset(registered_tables)


def test_message_role_check_constraint(isolated_db):
    """Verify Message role accepts only 'user', 'assistant', 'system'."""
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        user = User(name="Role Tester")
        session = Session(user=user, title="Role Test Session")
        db.add_all([user, session])
        db.commit()

        # Valid roles should succeed
        for valid_role in ["user", "assistant", "system"]:
            msg = Message(session_id=session.id, role=valid_role, content=f"Hello as {valid_role}")
            db.add(msg)
            db.commit()

        # Invalid role should be rejected by CheckConstraint
        invalid_msg = Message(session_id=session.id, role="superuser", content="Should fail")
        db.add(invalid_msg)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()


def test_timestamp_update_behavior(isolated_db):
    """Verify updated_at updates on record modification while created_at remains unchanged."""
    import time
    SessionLocal = isolated_db["session_factory"]
    with SessionLocal() as db:
        user = User(name="Initial Name")
        db.add(user)
        db.commit()
        db.refresh(user)

        initial_created = user.created_at
        initial_updated = user.updated_at

        time.sleep(0.01)
        user.name = "Updated Name"
        db.commit()
        db.refresh(user)

        assert user.created_at == initial_created
        assert user.updated_at >= initial_updated


def test_model_repr_methods(isolated_db):
    """Verify model string representations are informative and do not leak code in DebugHistory."""
    user = User(id="u1", name="Test User")
    session = Session(id="s1", user_id="u1", title="Test Session", status="active")
    msg = Message(id="m1", session_id="s1", role="user", content="Secret Prompt")
    saved = SavedMessage(id="sm1", user_id="u1", message_id="m1")
    note = Note(id="n1", user_id="u1", title="Test Note", content="Notes")
    code = GeneratedCode(id="c1", session_id="s1", language="python", code="secret_code()")
    debug = DebugHistory(
        id="d1",
        session_id="s1",
        original_code="secret_orig_code()",
        error_message="err",
        corrected_code="secret_fixed_code()",
        validation_status="passed",
        attempt_count=2,
    )

    assert "<User" in repr(user)
    assert "<Session" in repr(session)
    assert "<Message" in repr(msg)
    assert "<SavedMessage" in repr(saved)
    assert "<Note" in repr(note)
    assert "<GeneratedCode" in repr(code)
    assert "<DebugHistory" in repr(debug)

    # Verify sensitive source code is NOT included in DebugHistory.__repr__
    debug_repr = repr(debug)
    assert "secret_orig_code" not in debug_repr
    assert "secret_fixed_code" not in debug_repr


def test_schema_primary_keys_and_foreign_keys(isolated_db):
    """Verify primary keys and foreign key constraints on all 7 tables via inspection."""
    engine = isolated_db["engine"]
    inspector = inspect(engine)

    expected_tables = [
        "users",
        "sessions",
        "messages",
        "saved_messages",
        "notes",
        "generated_code",
        "debug_history",
    ]

    for table in expected_tables:
        pk = inspector.get_pk_constraint(table)
        assert pk["constrained_columns"] == ["id"], f"Table {table} does not have 'id' as primary key"

    # Verify foreign keys
    sessions_fks = {fk["referred_table"] for fk in inspector.get_foreign_keys("sessions")}
    assert "users" in sessions_fks

    messages_fks = {fk["referred_table"] for fk in inspector.get_foreign_keys("messages")}
    assert "sessions" in messages_fks

    saved_fks = {fk["referred_table"] for fk in inspector.get_foreign_keys("saved_messages")}
    assert {"users", "messages"}.issubset(saved_fks)

    code_fks = {fk["referred_table"] for fk in inspector.get_foreign_keys("generated_code")}
    assert {"sessions", "messages"}.issubset(code_fks)

    debug_fks = {fk["referred_table"] for fk in inspector.get_foreign_keys("debug_history")}
    assert "sessions" in debug_fks

