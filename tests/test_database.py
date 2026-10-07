import os
import tempfile
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import settings
from backend.app.database.engine import (
    create_db_engine,
    init_db,
    check_db_connection,
    get_engine_args,
)


def test_database_url_configuration():
    """Verify DATABASE_URL is loaded from settings and configurable."""
    assert settings.DATABASE_URL is not None
    assert "sqlite" in settings.DATABASE_URL


def test_sqlite_engine_arguments():
    """Verify SQLite connect args enforce check_same_thread=False for local development."""
    sqlite_args = get_engine_args("sqlite:///./data/test.db")
    assert sqlite_args["connect_args"]["check_same_thread"] is False

    other_args = get_engine_args("postgresql://user:pass@localhost/db")
    assert other_args["connect_args"] == {}


def test_database_connection_and_select_1():
    """Verify an isolated database engine connects and executes SELECT 1."""
    test_engine = create_db_engine("sqlite:///:memory:")
    assert check_db_connection(target_engine=test_engine) is True
    test_engine.dispose()


def test_session_factory_isolated():
    """Verify session factory operates against an isolated database."""
    test_engine = create_db_engine("sqlite:///:memory:")
    TestSession = sessionmaker(bind=test_engine)

    with TestSession() as session:
        result = session.execute(text("SELECT 1")).scalar()
        assert result == 1
    test_engine.dispose()


def test_database_creation_in_temp_dir():
    """Verify database initialization creates a missing SQLite file in the configured directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_db_path = os.path.join(tmp_dir, "isolated_test.db")
        test_url = f"sqlite:///{test_db_path}"

        assert not os.path.exists(test_db_path)

        test_engine = create_db_engine(test_url)
        init_db(target_engine=test_engine, url=test_url)

        # Verify file was created
        assert os.path.exists(test_db_path)
        assert os.path.getsize(test_db_path) >= 0
        test_engine.dispose()


def test_existing_database_not_destructively_recreated():
    """Verify running init_db on an existing database does not destroy data."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_db_path = os.path.join(tmp_dir, "existing_test.db")
        test_url = f"sqlite:///{test_db_path}"
        test_engine = create_db_engine(test_url)

        # First initialization
        init_db(target_engine=test_engine, url=test_url)
        with test_engine.connect() as conn:
            conn.execute(text("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT);"))
            conn.execute(text("INSERT INTO test_table (name) VALUES ('persistent_item');"))
            conn.commit()

        # Re-run initialization
        init_db(target_engine=test_engine, url=test_url)

        # Verify table and record still exist
        with test_engine.connect() as conn:
            row = conn.execute(text("SELECT name FROM test_table WHERE id=1;")).fetchone()
            assert row is not None
            assert row[0] == "persistent_item"

        test_engine.dispose()


def test_database_restart_persistence():
    """Verify restarting/recreating engine against same file preserves data."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_db_path = os.path.join(tmp_dir, "restart_test.db")
        test_url = f"sqlite:///{test_db_path}"

        engine1 = create_db_engine(test_url)
        with engine1.connect() as conn:
            conn.execute(text("CREATE TABLE counter (val INTEGER);"))
            conn.execute(text("INSERT INTO counter (val) VALUES (42);"))
            conn.commit()
        engine1.dispose()

        # Re-open with new engine instance
        engine2 = create_db_engine(test_url)
        with engine2.connect() as conn:
            val = conn.execute(text("SELECT val FROM counter;")).scalar()
            assert val == 42
        engine2.dispose()
