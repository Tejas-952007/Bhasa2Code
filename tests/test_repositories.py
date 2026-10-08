import os
import tempfile
import uuid
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from backend.app.database.engine import init_db, get_engine_args
from backend.app.database.repositories import (
    UserRepository,
    SessionRepository,
    MessageRepository,
    SavedMessageRepository,
    NoteRepository,
    GeneratedCodeRepository,
    DebugHistoryRepository,
)


@pytest.fixture
def test_db_session():
    """Create an isolated temporary SQLite database and yield an active session."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_repos.db")
        db_url = f"sqlite:///{db_path}"
        test_engine = create_engine(db_url, **get_engine_args(db_url))

        # Enforce foreign key constraints
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


# ---------------------------------------------------------------------------
# 1. User Repository Tests
# ---------------------------------------------------------------------------

def test_user_repository_crud(test_db_session):
    repo = UserRepository(test_db_session)

    # Create
    user = repo.create(name="Rohan")
    assert user.id is not None
    assert user.name == "Rohan"
    assert repo.exists(user.id) is True

    # Get by ID
    fetched = repo.get_by_id(user.id)
    assert fetched is not None
    assert fetched.name == "Rohan"

    # Alias check
    assert repo.get_user_by_id(user.id).name == "Rohan"

    # List
    users = repo.list_users()
    assert len(users) >= 1
    assert any(u.id == user.id for u in users)

    # Update
    updated = repo.update(user.id, name="Rohan Joshi")
    assert updated is not None
    assert updated.name == "Rohan Joshi"

    # Delete
    deleted = repo.delete_user(user.id)
    assert deleted is True
    assert repo.get_by_id(user.id) is None
    assert repo.exists(user.id) is False

    # Delete nonexistent
    assert repo.delete("nonexistent-id") is False


# ---------------------------------------------------------------------------
# 2. Session Repository Tests
# ---------------------------------------------------------------------------

def test_session_repository_crud_and_search(test_db_session):
    user_repo = UserRepository(test_db_session)
    session_repo = SessionRepository(test_db_session)

    user = user_repo.create(name="Pooja")

    # Create
    s1 = session_repo.create(
        user_id=user.id,
        title="Python Basics",
        programming_language="python",
    )
    s2 = session_repo.create(
        user_id=user.id,
        title="Django REST Setup",
        programming_language="python",
    )
    assert s1.id is not None
    assert s2.id is not None

    # Get by ID
    assert session_repo.get_by_id(s1.id) is not None
    assert session_repo.get_by_id(s1.id, user_id=user.id) is not None
    # User ownership isolation
    assert session_repo.get_by_id(s1.id, user_id="random-user-id") is None

    # List by user (ordered updated_at DESC)
    sessions = session_repo.list_by_user(user.id)
    assert len(sessions) == 2

    # Update
    updated = session_repo.update(
        s1.id,
        user_id=user.id,
        title="Python Advanced Concepts",
        status="completed",
    )
    assert updated is not None
    assert updated.title == "Python Advanced Concepts"
    assert updated.status == "completed"

    # Cross-user update blocked
    assert session_repo.update(s1.id, user_id="wrong-user", title="Hacked") is None

    # Search
    search_results = session_repo.search(user.id, "Advanced")
    assert len(search_results) == 1
    assert search_results[0].id == s1.id

    search_empty = session_repo.search(user.id, "NonexistentTerm")
    assert len(search_empty) == 0

    # Delete with ownership check
    assert session_repo.delete(s2.id, user_id="wrong-user") is False
    assert session_repo.delete(s2.id, user_id=user.id) is True
    assert session_repo.get_by_id(s2.id) is None


# ---------------------------------------------------------------------------
# 3. Message Repository Tests
# ---------------------------------------------------------------------------

def test_message_repository_ordering_and_isolation(test_db_session):
    user_repo = UserRepository(test_db_session)
    session_repo = SessionRepository(test_db_session)
    msg_repo = MessageRepository(test_db_session)

    user = user_repo.create(name="Anil")
    sess1 = session_repo.create(user_id=user.id, title="Session 1")
    sess2 = session_repo.create(user_id=user.id, title="Session 2")

    # Create messages in Session 1
    m1 = msg_repo.create(
        session_id=sess1.id,
        role="user",
        content="palindrome program dakhva",
        detected_language="marathi",
    )
    m2 = msg_repo.create(
        session_id=sess1.id,
        role="assistant",
        content="Here is the palindrome code in Python",
        programming_language="python",
    )

    # Create message in Session 2
    m3 = msg_repo.create(
        session_id=sess2.id,
        role="user",
        content="bubble sort samjhava",
        detected_language="marathi",
    )

    # Session 1 listing should have m1 then m2 (created_at ASC)
    s1_msgs = msg_repo.list_by_session(sess1.id)
    assert len(s1_msgs) == 2
    assert s1_msgs[0].id == m1.id
    assert s1_msgs[1].id == m2.id

    # Session isolation: sess1 list must NOT contain m3
    assert all(m.session_id == sess1.id for m in s1_msgs)
    assert not any(m.id == m3.id for m in s1_msgs)

    # Session 2 listing
    s2_msgs = msg_repo.list_by_session(sess2.id)
    assert len(s2_msgs) == 1
    assert s2_msgs[0].id == m3.id

    # Search in Session 1
    search_palindrome = msg_repo.search(sess1.id, "palindrome")
    assert len(search_palindrome) == 2

    search_dakhva = msg_repo.search(sess1.id, "dakhva")
    assert len(search_dakhva) == 1
    assert search_dakhva[0].id == m1.id

    search_other_session_content = msg_repo.search(sess1.id, "bubble")
    assert len(search_other_session_content) == 0

    # Latest message
    latest = msg_repo.get_latest_message(sess1.id)
    assert latest is not None
    assert latest.id == m2.id

    # Count
    assert msg_repo.count_by_session(sess1.id) == 2
    assert msg_repo.count_by_session(sess2.id) == 1

    # Delete scoped by session
    assert msg_repo.delete(m1.id, session_id=sess2.id) is False  # Wrong session
    assert msg_repo.delete(m1.id, session_id=sess1.id) is True
    assert msg_repo.get_by_id(m1.id) is None


# ---------------------------------------------------------------------------
# 4. Saved Message Repository Tests
# ---------------------------------------------------------------------------

def test_saved_message_repository_idempotency_and_unsave(test_db_session):
    user_repo = UserRepository(test_db_session)
    session_repo = SessionRepository(test_db_session)
    msg_repo = MessageRepository(test_db_session)
    saved_repo = SavedMessageRepository(test_db_session)

    user = user_repo.create(name="Deepak")
    session = session_repo.create(user_id=user.id, title="Algorithm Study")
    msg = msg_repo.create(session_id=session.id, role="assistant", content="Useful snippet")

    # Initial save
    saved = saved_repo.save_message(user_id=user.id, message_id=msg.id, label="Key Concept")
    assert saved.id is not None
    assert saved.label == "Key Concept"
    assert saved_repo.is_saved(user.id, msg.id) is True

    # Duplicate save with updated label should be idempotent
    saved_again = saved_repo.save_message(user_id=user.id, message_id=msg.id, label="Updated Label")
    assert saved_again.id == saved.id
    assert saved_again.label == "Updated Label"

    # List saved messages
    saved_list = saved_repo.list_saved_messages(user.id)
    assert len(saved_list) == 1
    assert saved_list[0].message_id == msg.id

    # Unsave
    unsaved = saved_repo.unsave_message(user.id, msg.id)
    assert unsaved is True
    assert saved_repo.is_saved(user.id, msg.id) is False
    assert saved_repo.get_saved_message(user.id, msg.id) is None

    # Unsave nonexistent
    assert saved_repo.unsave_message(user.id, "fake-msg") is False


# ---------------------------------------------------------------------------
# 5. Note Repository Tests
# ---------------------------------------------------------------------------

def test_note_repository_crud_search_isolation(test_db_session):
    user_repo = UserRepository(test_db_session)
    session_repo = SessionRepository(test_db_session)
    note_repo = NoteRepository(test_db_session)

    user1 = user_repo.create(name="User 1")
    user2 = user_repo.create(name="User 2")
    session1 = session_repo.create(user_id=user1.id, title="Sess 1")

    # Create note
    n1 = note_repo.create(
        user_id=user1.id,
        title="Recursion Notes",
        content="Base condition is essential",
        session_id=session1.id,
    )
    n2 = note_repo.create(
        user_id=user1.id,
        title="Dynamic Programming",
        content="Memoization vs Tabulation",
    )
    assert n1.id is not None
    assert n2.id is not None

    # List notes by user
    u1_notes = note_repo.list_notes_by_user(user1.id)
    assert len(u1_notes) == 2

    # Filter by session
    sess_notes = note_repo.list_notes_by_user(user1.id, session_id=session1.id)
    assert len(sess_notes) == 1
    assert sess_notes[0].id == n1.id

    # Search notes
    results = note_repo.search(user1.id, "Memoization")
    assert len(results) == 1
    assert results[0].id == n2.id

    # Ownership isolation: user2 cannot get user1's note
    assert note_repo.get_by_id(n1.id, user_id=user2.id) is None
    assert note_repo.update(n1.id, user_id=user2.id, title="Hijacked") is None
    assert note_repo.delete(n1.id, user_id=user2.id) is False

    # Valid update
    updated = note_repo.update(n1.id, user_id=user1.id, title="Recursion & Backtracking")
    assert updated is not None
    assert updated.title == "Recursion & Backtracking"

    # Valid delete
    assert note_repo.delete(n1.id, user_id=user1.id) is True
    assert note_repo.get_by_id(n1.id) is None


# ---------------------------------------------------------------------------
# 6. Generated Code Repository Tests
# ---------------------------------------------------------------------------

def test_generated_code_repository_crud(test_db_session):
    user_repo = UserRepository(test_db_session)
    session_repo = SessionRepository(test_db_session)
    msg_repo = MessageRepository(test_db_session)
    code_repo = GeneratedCodeRepository(test_db_session)

    user = user_repo.create(name="Sneha")
    session = session_repo.create(user_id=user.id, title="CodeGen Session")
    msg = msg_repo.create(session_id=session.id, role="assistant", content="Here is code")

    code_record = code_repo.create(
        session_id=session.id,
        message_id=msg.id,
        code="def solve(): pass",
        language="python",
        validation_status="unvalidated",
    )
    assert code_record.id is not None
    assert code_record.validation_status == "unvalidated"

    # Get by ID
    assert code_repo.get_by_id(code_record.id) is not None

    # Get by message ID
    by_msg = code_repo.get_code_for_message(msg.id)
    assert len(by_msg) == 1
    assert by_msg[0].id == code_record.id

    # List by session
    by_sess = code_repo.list_code_by_session(session.id)
    assert len(by_sess) == 1
    assert by_sess[0].id == code_record.id

    # Update status
    updated = code_repo.update_validation_status(code_record.id, "valid")
    assert updated is not None
    assert updated.validation_status == "valid"

    # Delete
    assert code_repo.delete(code_record.id) is True
    assert code_repo.get_by_id(code_record.id) is None


# ---------------------------------------------------------------------------
# 7. Debug History Repository Tests
# ---------------------------------------------------------------------------

def test_debug_history_repository_append_only(test_db_session):
    user_repo = UserRepository(test_db_session)
    session_repo = SessionRepository(test_db_session)
    msg_repo = MessageRepository(test_db_session)
    debug_repo = DebugHistoryRepository(test_db_session)

    user = user_repo.create(name="Kavita")
    session = session_repo.create(user_id=user.id, title="Debug Session")
    msg = msg_repo.create(session_id=session.id, role="assistant", content="Debug iteration")

    # Record attempt 1
    d1 = debug_repo.create(
        session_id=session.id,
        original_code="print(x)",
        error_message="NameError: name 'x' is not defined",
        corrected_code="x = 10\nprint(x)",
        validation_status="failed",
        attempt_count=1,
        message_id=msg.id,
    )

    # Record attempt 2
    d2 = debug_repo.create(
        session_id=session.id,
        original_code="x = 10\nprint(x)",
        error_message="",
        corrected_code="x = 10\nprint(x)",
        validation_status="success",
        attempt_count=2,
        message_id=msg.id,
    )

    # List by session in chronological order
    attempts = debug_repo.list_by_session(session.id)
    assert len(attempts) == 2
    assert attempts[0].id == d1.id
    assert attempts[1].id == d2.id

    # List by message
    msg_attempts = debug_repo.list_by_message(msg.id)
    assert len(msg_attempts) == 2

    # Latest debug record for session
    latest = debug_repo.get_latest_for_session(session.id)
    assert latest is not None
    assert latest.id == d2.id
    assert latest.attempt_count == 2


# ---------------------------------------------------------------------------
# 8. Cross-User Isolation Tests
# ---------------------------------------------------------------------------

def test_cross_user_isolation_strictly_enforced(test_db_session):
    user_repo = UserRepository(test_db_session)
    session_repo = SessionRepository(test_db_session)
    note_repo = NoteRepository(test_db_session)

    user_a = user_repo.create(name="User Alpha")
    user_b = user_repo.create(name="User Beta")

    session_a = session_repo.create(user_id=user_a.id, title="Alpha Private Work")
    note_a = note_repo.create(user_id=user_a.id, title="Alpha Secrets", content="Top secret")

    # User B attempting to read User A's session with ownership filter
    assert session_repo.get_by_id(session_a.id, user_id=user_b.id) is None

    # User B listing sessions must NOT contain User A's session
    user_b_sessions = session_repo.list_by_user(user_b.id)
    assert not any(s.id == session_a.id for s in user_b_sessions)

    # User B attempting to read User A's note
    assert note_repo.get_by_id(note_a.id, user_id=user_b.id) is None

    # User B listing notes must NOT contain User A's note
    user_b_notes = note_repo.list_notes_by_user(user_b.id)
    assert not any(n.id == note_a.id for n in user_b_notes)


# ---------------------------------------------------------------------------
# 9. Transaction Rollback on Failure
# ---------------------------------------------------------------------------

def test_transaction_rollback_preserves_state(test_db_session):
    user_repo = UserRepository(test_db_session)
    session_repo = SessionRepository(test_db_session)

    user = user_repo.create(name="Rollback Test User")
    initial_user_count = user_repo.count()

    # Forcing a database IntegrityError: Session with invalid foreign key
    with pytest.raises(IntegrityError):
        session_repo.create(
            user_id="nonexistent-foreign-user-id",
            title="Invalid Session",
        )

    # The session must have rolled back cleanly and not leave broken state
    # Verify that the session is usable immediately after the failure
    assert user_repo.count() == initial_user_count
    valid_session = session_repo.create(user_id=user.id, title="Valid Post-Rollback Session")
    assert valid_session.id is not None
    assert session_repo.exists(valid_session.id) is True


# ---------------------------------------------------------------------------
# 10. Deferred Commit Workflow (commit=False)
# ---------------------------------------------------------------------------

def test_deferred_commit_multi_entity_transaction(test_db_session):
    user_repo = UserRepository(test_db_session)
    session_repo = SessionRepository(test_db_session)
    msg_repo = MessageRepository(test_db_session)

    user = user_repo.create(name="Atomic User", commit=False)
    session = session_repo.create(user_id=user.id, title="Atomic Session", commit=False)
    msg = msg_repo.create(session_id=session.id, role="user", content="Hello", commit=False)

    # Commit all atomically at service/session level
    test_db_session.commit()

    assert user_repo.exists(user.id) is True
    assert session_repo.exists(session.id) is True
    assert msg_repo.exists(msg.id) is True
