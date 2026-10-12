"""Python syntax and ML consistency validator using stdlib ast."""

import ast
from typing import Any, Dict, List, Optional, Set

from backend.app.validation.schemas import (
    CodeValidationResult,
    ValidationDiagnostic,
    ValidationStatus,
)
from backend.app.validation.validators.base import BaseCodeValidator


class MLCodeConsistencyChecker(ast.NodeVisitor):
    """Static AST consistency checks for machine learning pipelines."""

    def __init__(self) -> None:
        self.diagnostics: List[ValidationDiagnostic] = []
        self.vectorizer_instances: Set[str] = set()
        self.vectorizer_pipelines: Set[str] = set()
        self.pre_vectorized_vars: Set[str] = set()
        self.vectorizer_var_sources: Dict[str, str] = {}
        self.literal_lists: Dict[str, List[Any]] = {}
        self.string_label_vars: Set[str] = set()
        self.prediction_vars: Set[str] = set()

    def visit_Assign(self, node: ast.Assign) -> None:
        val_repr = ast.unparse(node.value) if hasattr(ast, "unparse") else ""

        # Track vectorizer instance assignments: vec = TfidfVectorizer()
        if any(vec in val_repr for vec in ("TfidfVectorizer", "CountVectorizer", "HashingVectorizer")):
            if "Pipeline" not in val_repr and not any(m in val_repr for m in (".fit_transform", ".transform")):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.vectorizer_instances.add(target.id)

        # Track literal lists
        if isinstance(node.value, ast.List):
            items = []
            for elt in node.value.elts:
                if isinstance(elt, ast.Constant):
                    items.append(elt.value)
                else:
                    items.append(None)
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.literal_lists[target.id] = items
                    if items and all(isinstance(x, str) for x in items if x is not None):
                        self.string_label_vars.add(target.id)

        # Track fit_transform / transform calls
        if isinstance(node.value, ast.Call):
            call = node.value
            func_name = ""
            caller_name = ""
            if isinstance(call.func, ast.Attribute):
                func_name = call.func.attr
                caller_name = ast.unparse(call.func.value) if hasattr(ast, "unparse") else ""
            elif isinstance(call.func, ast.Name):
                func_name = call.func.id

            if func_name in ("fit_transform", "transform") and (
                caller_name in self.vectorizer_instances
                or any(vec in val_repr for vec in ("TfidfVectorizer", "CountVectorizer", "HashingVectorizer"))
            ):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.pre_vectorized_vars.add(target.id)
                        if call.args:
                            self.vectorizer_var_sources[target.id] = ast.unparse(call.args[0])

            # Track prediction assignments: res = pipeline.predict(...)
            if func_name == "predict":
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.prediction_vars.add(target.id)

            # Detect Pipeline with vectorizer
            if "Pipeline" in val_repr and any(
                vec in val_repr for vec in ("TfidfVectorizer", "CountVectorizer", "HashingVectorizer")
            ):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.vectorizer_pipelines.add(target.id)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Attribute):
            method_name = func.attr
            caller_name = ast.unparse(func.value) if hasattr(ast, "unparse") else ""

            # Check .fit(X, y) calls
            if method_name == "fit" and len(node.args) >= 2:
                arg0, arg1 = node.args[0], node.args[1]
                arg0_repr = ast.unparse(arg0) if hasattr(ast, "unparse") else ""
                arg1_repr = ast.unparse(arg1) if hasattr(ast, "unparse") else ""

                is_text_pipeline = (
                    caller_name in self.vectorizer_pipelines
                    or "pipeline" in caller_name.lower()
                )

                # 1. Target is identical to features
                if arg0_repr and arg0_repr == arg1_repr:
                    self.diagnostics.append(
                        ValidationDiagnostic(
                            severity="ERROR",
                            message=f"Target labels y cannot be identical to input features X ({caller_name}.fit({arg0_repr}, {arg1_repr})). Target labels must represent distinct class categories.",
                            line=node.lineno,
                        )
                    )
                # 2. Target is the text source that was used to produce X
                elif (
                    arg0_repr in self.vectorizer_var_sources
                    and self.vectorizer_var_sources[arg0_repr] == arg1_repr
                ):
                    self.diagnostics.append(
                        ValidationDiagnostic(
                            severity="ERROR",
                            message=f"Model is trained to predict input text instead of target labels ({caller_name}.fit({arg0_repr}, {arg1_repr})). Target labels y must be ground-truth classes.",
                            line=node.lineno,
                        )
                    )
                # 3. Duplicate vectorization into Pipeline
                elif is_text_pipeline and (
                    arg0_repr in self.pre_vectorized_vars
                    or any(v in arg0_repr for v in ("fit_transform", "transform"))
                ):
                    self.diagnostics.append(
                        ValidationDiagnostic(
                            severity="ERROR",
                            message=f"Duplicate text vectorization: features '{arg0_repr}' were already transformed by a vectorizer, but '{caller_name}' already contains a text vectorizer step. Pass raw text strings directly to pipeline.fit().",
                            line=node.lineno,
                        )
                    )

                # 4. Literal sample count mismatch
                if (
                    isinstance(arg0, ast.Name)
                    and isinstance(arg1, ast.Name)
                    and arg0.id in self.literal_lists
                    and arg1.id in self.literal_lists
                ):
                    len0 = len(self.literal_lists[arg0.id])
                    len1 = len(self.literal_lists[arg1.id])
                    if len0 != len1:
                        self.diagnostics.append(
                            ValidationDiagnostic(
                                severity="ERROR",
                                message=f"Inconsistent sample count: feature dataset '{arg0.id}' has {len0} samples, but target labels list '{arg1.id}' has {len1} samples (must have equal length).",
                                line=node.lineno,
                            )
                        )

            # Check .predict(input_data) calls
            if method_name == "predict" and node.args:
                arg0 = node.args[0]
                # Check for nested 2D list of strings: predict([['sample text']])
                if isinstance(arg0, ast.List) and arg0.elts:
                    first_elt = arg0.elts[0]
                    if isinstance(first_elt, ast.List) and first_elt.elts:
                        inner_first = first_elt.elts[0]
                        if isinstance(inner_first, ast.Constant) and isinstance(inner_first.value, str):
                            self.diagnostics.append(
                                ValidationDiagnostic(
                                    severity="ERROR",
                                    message=f"{caller_name}.predict() received nested 2D list of text [[...]]. Text classification pipelines require a 1D list of raw strings ['...'].",
                                    line=node.lineno,
                                )
                            )

        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        # Check if assertion compares prediction with integer constant when target was strings
        test_expr = node.test
        if isinstance(test_expr, ast.Compare):
            left_repr = ast.unparse(test_expr.left) if hasattr(ast, "unparse") else ""
            is_pred_check = "predict" in left_repr or any(pv in left_repr for pv in self.prediction_vars)
            if is_pred_check:
                for comparator in test_expr.comparators:
                    if isinstance(comparator, ast.Constant) and isinstance(comparator.value, int):
                        self.diagnostics.append(
                            ValidationDiagnostic(
                                severity="ERROR",
                                message=f"Assertion compares text model prediction with numeric literal {comparator.value}, but model was trained on string labels. Assert against string class labels.",
                                line=node.lineno,
                            )
                        )
        self.generic_visit(node)


class PythonValidator(BaseCodeValidator):
    """Validates Python syntax and ML consistency statically using standard library AST parser."""

    language = "python"

    def validate(self, code: str, block_id: int = 1) -> CodeValidationResult:
        """Parse Python source code using ast.parse without executing any statements."""
        if not code or not code.strip():
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.VALID,
                code=code,
                diagnostics=[],
            )

        try:
            # ast.parse does not execute code; it purely builds the syntax tree
            tree = ast.parse(code)
            checker = MLCodeConsistencyChecker()
            checker.visit(tree)
            diagnostics = checker.diagnostics

            has_error = any(d.severity == "ERROR" for d in diagnostics)
            status = ValidationStatus.INVALID if has_error else ValidationStatus.VALID

            return self.create_result(
                block_id=block_id,
                status=status,
                code=code,
                diagnostics=diagnostics,
            )
        except (SyntaxError, IndentationError) as err:
            diagnostic = ValidationDiagnostic(
                severity="ERROR",
                message=err.msg or str(err),
                line=err.lineno,
                column=err.offset,
                code=err.text.strip() if err.text else None,
            )
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.INVALID,
                code=code,
                diagnostics=[diagnostic],
            )
        except Exception as err:
            diagnostic = ValidationDiagnostic(
                severity="ERROR",
                message=f"Parser error: {err}",
            )
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.INVALID,
                code=code,
                diagnostics=[diagnostic],
            )

