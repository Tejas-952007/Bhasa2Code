"""Unit tests for SQLValidator."""

from backend.app.validation.schemas import ValidationStatus
from backend.app.validation.validators.sql_validator import SQLValidator


def test_sql_valid_statements():
    validator = SQLValidator()

    # Valid SELECT
    res = validator.validate("SELECT id, name FROM users WHERE age > 18;")
    assert res.status == ValidationStatus.VALID

    # Valid INSERT
    res = validator.validate("INSERT INTO students (id, name) VALUES (1, 'Rahul');")
    assert res.status == ValidationStatus.VALID

    # Valid UPDATE
    res = validator.validate("UPDATE employees SET salary = salary * 1.1 WHERE department = 'Engineering';")
    assert res.status == ValidationStatus.VALID

    # Valid DELETE
    res = validator.validate("DELETE FROM temp_logs WHERE created_at < '2026-01-01';")
    assert res.status == ValidationStatus.VALID

    # Valid CREATE TABLE
    res = validator.validate("CREATE TABLE products (id INT PRIMARY KEY, name VARCHAR(100), price DECIMAL(10, 2));")
    assert res.status == ValidationStatus.VALID


def test_sql_unclosed_quotes():
    validator = SQLValidator()
    code = "SELECT * FROM users WHERE name = 'John;"
    res = validator.validate(code)
    assert res.status == ValidationStatus.INVALID
    assert any("quote" in d.message.lower() for d in res.diagnostics)


def test_sql_unclosed_parentheses():
    validator = SQLValidator()
    code = "INSERT INTO users (id, name VALUES (1, 'Alice');"
    res = validator.validate(code)
    assert res.status == ValidationStatus.INVALID
    assert any("parenthesis" in d.message.lower() for d in res.diagnostics)


def test_sql_missing_table_or_clauses():
    validator = SQLValidator()

    # Incomplete SELECT
    res = validator.validate("SELECT * FROM ;")
    assert res.status == ValidationStatus.INVALID

    # Incomplete INSERT
    res = validator.validate("INSERT INTO ;")
    assert res.status == ValidationStatus.INVALID

    # Incomplete UPDATE
    res = validator.validate("UPDATE users SET ;")
    assert res.status == ValidationStatus.INVALID


def test_sql_comments_stripped():
    validator = SQLValidator()
    code = (
        "-- Fetch active users\n"
        "SELECT id, name /* columns */ FROM users;\n"
    )
    res = validator.validate(code)
    assert res.status == ValidationStatus.VALID


def test_sql_unsupported_statement():
    validator = SQLValidator()
    code = "EXPLAIN QUERY PLAN SELECT 1;"
    res = validator.validate(code)
    assert res.status == ValidationStatus.UNSUPPORTED
