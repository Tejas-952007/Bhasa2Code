"""Orchestrator for extracting and validating code in assistant responses."""

import logging
from typing import Dict, List, Optional

from backend.app.validation.code_extractor import CodeExtractor
from backend.app.validation.language_resolver import resolve_language
from backend.app.validation.schemas import (
    CodeValidationResult,
    ResponseValidationResult,
    ValidationDiagnostic,
    ValidationStatus,
)
from backend.app.validation.validators import (
    BaseCodeValidator,
    CValidator,
    CppValidator,
    JavaValidator,
    JavaScriptValidator,
    PythonValidator,
    SQLValidator,
)

logger = logging.getLogger(__name__)


class ResponseValidator:
    """Validates coding assistant responses by extracting and verifying code syntax."""

    def __init__(
        self,
        extractor: Optional[CodeExtractor] = None,
        validators: Optional[Dict[str, BaseCodeValidator]] = None,
    ) -> None:
        self.extractor = extractor or CodeExtractor()
        self.validators = validators or self._default_validators()

    def _default_validators(self) -> Dict[str, BaseCodeValidator]:
        """Instantiate default suite of static validators."""
        return {
            "python": PythonValidator(),
            "c": CValidator(),
            "cpp": CppValidator(),
            "java": JavaValidator(),
            "javascript": JavaScriptValidator(),
            "sql": SQLValidator(),
        }

    def validate(
        self,
        response_text: str,
        language_hint: Optional[str] = None,
    ) -> ResponseValidationResult:
        """Parse response text, extract code blocks, and perform syntax validation.

        Args:
            response_text: Raw assistant response text.
            language_hint: Optional programming language hint from upstream context/NLP.

        Returns:
            ResponseValidationResult containing aggregate status, block details, and diagnostics.

        Raises:
            ValueError: If response_text is None.
        """
        if response_text is None:
            raise ValueError("response_text cannot be None.")

        # 1. Extract fenced and structured code blocks
        raw_blocks = self.extractor.extract_blocks(response_text)

        if not raw_blocks:
            return ResponseValidationResult(
                status=ValidationStatus.NOT_VALIDATED,
                original_response=response_text,
                code_blocks=[],
                diagnostics=[],
                has_code=False,
            )

        # 2. Validate each individual block
        validated_blocks: List[CodeValidationResult] = []
        all_diagnostics: List[ValidationDiagnostic] = []

        for block in raw_blocks:
            # Resolve language using priority: fence -> hint -> heuristics -> None
            resolved_lang = resolve_language(
                declared_language=block.declared_language,
                code=block.code,
                language_hint=language_hint,
            )
            block.resolved_language = resolved_lang

            if resolved_lang and resolved_lang in self.validators:
                validator = self.validators[resolved_lang]
                block_res = validator.validate(block.code, block_id=block.block_id)
                # Ensure resolved language is preserved in result
                block_res.language = resolved_lang
            else:
                target_lang_label = resolved_lang or block.declared_language or "unknown"
                block_res = CodeValidationResult(
                    block_id=block.block_id,
                    language=resolved_lang or block.declared_language,
                    status=ValidationStatus.UNSUPPORTED,
                    code=block.code,
                    diagnostics=[
                        ValidationDiagnostic(
                            severity="INFO",
                            message=f"No static validator available for language '{target_lang_label}'.",
                        )
                    ],
                    validator="None",
                )

            validated_blocks.append(block_res)
            all_diagnostics.extend(block_res.diagnostics)

        # 3. Aggregate statuses deterministically
        aggregated_status = self._aggregate_statuses([b.status for b in validated_blocks])

        logger.info(
            "Response validation finished: status=%s blocks=%d diagnostics=%d",
            aggregated_status,
            len(validated_blocks),
            len(all_diagnostics),
        )

        return ResponseValidationResult(
            status=aggregated_status,
            original_response=response_text,
            code_blocks=validated_blocks,
            diagnostics=all_diagnostics,
            has_code=True,
        )

    def _aggregate_statuses(self, statuses: List[ValidationStatus]) -> ValidationStatus:
        """Deterministic status aggregation rules:

        - No blocks: NOT_VALIDATED
        - Any INVALID: INVALID (strict failure propagation)
        - All VALID: VALID
        - All UNSUPPORTED: UNSUPPORTED
        - Mixture of VALID and UNSUPPORTED: UNSUPPORTED (cannot certify partial unknown)
        - Mixture of VALID and INVALID: INVALID
        """
        if not statuses:
            return ValidationStatus.NOT_VALIDATED

        if any(s == ValidationStatus.INVALID for s in statuses):
            return ValidationStatus.INVALID

        if all(s == ValidationStatus.VALID for s in statuses):
            return ValidationStatus.VALID

        if all(s == ValidationStatus.UNSUPPORTED for s in statuses):
            return ValidationStatus.UNSUPPORTED

        if any(s == ValidationStatus.UNSUPPORTED for s in statuses):
            return ValidationStatus.UNSUPPORTED

        return ValidationStatus.NOT_VALIDATED
