"""Deterministic static SQL syntax validator for standard SQL statements."""

import re
from typing import List

from backend.app.validation.schemas import CodeValidationResult, ValidationDiagnostic, ValidationStatus
from backend.app.validation.validators.base import BaseCodeValidator


class SQLValidator(BaseCodeValidator):
    """Deterministic structural validator for standard SQL statements without DB execution."""

    language = "sql"

    def validate(self, code: str, block_id: int = 1) -> CodeValidationResult:
        """Validate basic SQL syntax structure statically."""
        if not code or not code.strip():
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.VALID,
                code=code,
                diagnostics=[],
            )

        clean_sql = self._strip_comments(code).strip()
        if not clean_sql:
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.VALID,
                code=code,
                diagnostics=[],
            )

        # 1. Check quote balance
        quote_err = self._check_quotes(clean_sql)
        if quote_err:
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.INVALID,
                code=code,
                diagnostics=[ValidationDiagnostic(severity="ERROR", message=quote_err)],
            )

        # 2. Check parentheses balance
        paren_err = self._check_parentheses(clean_sql)
        if paren_err:
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.INVALID,
                code=code,
                diagnostics=[ValidationDiagnostic(severity="ERROR", message=paren_err)],
            )

        # 3. Check individual statements (separated by semicolon)
        statements = [s.strip() for s in clean_sql.split(";") if s.strip()]
        if not statements:
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.VALID,
                code=code,
                diagnostics=[],
            )

        for stmt in statements:
            status, err_msg = self._validate_statement(stmt)
            if status == ValidationStatus.INVALID:
                return self.create_result(
                    block_id=block_id,
                    status=ValidationStatus.INVALID,
                    code=code,
                    diagnostics=[
                        ValidationDiagnostic(
                            severity="ERROR",
                            message=err_msg or "SQL syntax structure error.",
                        )
                    ],
                )
            elif status == ValidationStatus.UNSUPPORTED:
                return self.create_result(
                    block_id=block_id,
                    status=ValidationStatus.UNSUPPORTED,
                    code=code,
                    diagnostics=[
                        ValidationDiagnostic(
                            severity="INFO",
                            message=err_msg or "SQL dialect or statement type unsupported for static verification.",
                        )
                    ],
                )

        return self.create_result(
            block_id=block_id,
            status=ValidationStatus.VALID,
            code=code,
            diagnostics=[],
        )

    def _strip_comments(self, sql: str) -> str:
        """Remove line and block comments from SQL."""
        # Remove /* block comments */
        no_blocks = re.sub(r"/\*[\s\S]*?\*/", "", sql)
        # Remove -- line comments
        no_lines = re.sub(r"--[^\n]*", "", no_blocks)
        return no_lines

    def _check_quotes(self, sql: str) -> str | None:
        """Check for unmatched single or double quotes."""
        in_single = False
        in_double = False
        prev_char = ""

        for char in sql:
            if char == "'" and not in_double and prev_char != "\\":
                in_single = not in_single
            elif char == '"' and not in_single and prev_char != "\\":
                in_double = not in_double
            prev_char = char

        if in_single:
            return "Unclosed single quote in SQL string literal."
        if in_double:
            return "Unclosed double quote in SQL identifier/string."
        return None

    def _check_parentheses(self, sql: str) -> str | None:
        """Verify matching parentheses depth outside quotes."""
        depth = 0
        in_quote = False
        quote_char = ""

        for char in sql:
            if char in ("'", '"'):
                if not in_quote:
                    in_quote = True
                    quote_char = char
                elif char == quote_char:
                    in_quote = False
            elif not in_quote:
                if char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                    if depth < 0:
                        return "Unexpected closing parenthesis ')' in SQL statement."

        if depth > 0:
            return "Unclosed opening parenthesis '(' in SQL statement."
        return None

    def _validate_statement(self, stmt: str) -> tuple[ValidationStatus, str | None]:
        """Validate structure of a single statement."""
        tokens = stmt.split()
        if not tokens:
            return ValidationStatus.VALID, None

        first_token = tokens[0].upper()

        if first_token == "SELECT":
            return self._validate_select(stmt, tokens)
        elif first_token == "INSERT":
            return self._validate_insert(stmt, tokens)
        elif first_token == "UPDATE":
            return self._validate_update(stmt, tokens)
        elif first_token == "DELETE":
            return self._validate_delete(stmt, tokens)
        elif first_token == "CREATE":
            return self._validate_create(stmt, tokens)
        elif first_token == "DROP":
            return self._validate_drop(stmt, tokens)
        elif first_token in ("ALTER", "TRUNCATE", "BEGIN", "COMMIT", "ROLLBACK", "USE"):
            return ValidationStatus.VALID, None
        else:
            return (
                ValidationStatus.UNSUPPORTED,
                f"Statement beginning with '{first_token}' is not supported by static SQL validator.",
            )

    def _validate_select(self, stmt: str, tokens: List[str]) -> tuple[ValidationStatus, str | None]:
        # SELECT cannot just be "SELECT" or "SELECT FROM"
        if len(tokens) < 2:
            return ValidationStatus.INVALID, "SELECT statement missing expressions or column list."
        if tokens[1].upper() == "FROM":
            return ValidationStatus.INVALID, "SELECT statement missing column expressions before FROM clause."

        # If FROM exists, check table following it
        upper_tokens = [t.upper() for t in tokens]
        if "FROM" in upper_tokens:
            from_idx = upper_tokens.index("FROM")
            if from_idx == len(tokens) - 1:
                return ValidationStatus.INVALID, "FROM clause missing table name."
            next_token = tokens[from_idx + 1]
            if next_token.upper() in ("WHERE", "GROUP", "ORDER", "HAVING", "LIMIT", ";"):
                return ValidationStatus.INVALID, f"FROM clause missing table name before '{next_token}'."

        # Cannot end with dangling operators like AND, OR, comma
        last_tok = tokens[-1].rstrip(";").upper()
        if last_tok in ("AND", "OR", "WHERE", "JOIN", ","):
            return ValidationStatus.INVALID, f"SELECT statement cannot terminate with dangling '{last_tok}'."

        return ValidationStatus.VALID, None

    def _validate_insert(self, stmt: str, tokens: List[str]) -> tuple[ValidationStatus, str | None]:
        # INSERT INTO <table> ...
        if len(tokens) < 3:
            return ValidationStatus.INVALID, "Incomplete INSERT statement."
        if tokens[1].upper() != "INTO":
            return ValidationStatus.INVALID, "INSERT statement missing INTO keyword."
        if tokens[2].upper() in ("VALUES", "SELECT", ";"):
            return ValidationStatus.INVALID, "INSERT INTO missing target table name."

        upper_stmt = stmt.upper()
        if "VALUES" not in upper_stmt and "SELECT" not in upper_stmt:
            return ValidationStatus.INVALID, "INSERT statement missing VALUES or SELECT clause."

        return ValidationStatus.VALID, None

    def _validate_update(self, stmt: str, tokens: List[str]) -> tuple[ValidationStatus, str | None]:
        # UPDATE <table> SET <col = val>
        if len(tokens) < 4:
            return ValidationStatus.INVALID, "Incomplete UPDATE statement."
        if tokens[1].upper() == "SET":
            return ValidationStatus.INVALID, "UPDATE statement missing target table name."
        if "SET" not in [t.upper() for t in tokens]:
            return ValidationStatus.INVALID, "UPDATE statement missing SET clause."

        upper_tokens = [t.upper() for t in tokens]
        set_idx = upper_tokens.index("SET")
        if set_idx == len(tokens) - 1:
            return ValidationStatus.INVALID, "SET clause missing assignment expressions."

        return ValidationStatus.VALID, None

    def _validate_delete(self, stmt: str, tokens: List[str]) -> tuple[ValidationStatus, str | None]:
        # DELETE FROM <table>
        if len(tokens) < 3:
            return ValidationStatus.INVALID, "Incomplete DELETE statement."
        if tokens[1].upper() != "FROM":
            return ValidationStatus.INVALID, "DELETE statement missing FROM keyword."
        if tokens[2].upper() in ("WHERE", ";"):
            return ValidationStatus.INVALID, "DELETE FROM missing target table name."

        return ValidationStatus.VALID, None

    def _validate_create(self, stmt: str, tokens: List[str]) -> tuple[ValidationStatus, str | None]:
        # CREATE TABLE [IF NOT EXISTS] <table> (...)
        upper_tokens = [t.upper() for t in tokens]
        if "TABLE" not in upper_tokens:
            return ValidationStatus.UNSUPPORTED, "CREATE statement other than CREATE TABLE."

        tbl_idx = upper_tokens.index("TABLE")
        if tbl_idx >= len(tokens) - 1:
            return ValidationStatus.INVALID, "CREATE TABLE missing table name."

        # Must have parentheses definition
        if "(" not in stmt or ")" not in stmt:
            return ValidationStatus.INVALID, "CREATE TABLE missing column definitions in parentheses."

        return ValidationStatus.VALID, None

    def _validate_drop(self, stmt: str, tokens: List[str]) -> tuple[ValidationStatus, str | None]:
        # DROP TABLE [IF EXISTS] <table>
        if len(tokens) < 3:
            return ValidationStatus.INVALID, "Incomplete DROP statement."
        return ValidationStatus.VALID, None
