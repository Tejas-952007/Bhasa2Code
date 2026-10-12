"""Regression tests for Bhasha2Code ML code generation, dependency availability, and sandbox isolation.

Verifies:
1. PythonRunner dynamic image and resource profile selection (python vs python_ml).
2. ML container execution with pinned packages (scikit-learn, numpy, scipy, pandas).
3. Small TF-IDF + Logistic Regression classification pipeline execution in isolated container.
4. Sandbox security invariants: non-root UID 1000, network disabled, capabilities dropped.
5. Error distinction: DEPENDENCY_ERROR vs VALIDATION_FAILED vs RUNTIME_ERROR.
6. PromptBuilder ML task directives: feature/label separation, pipeline raw-text inputs, exact sample counts.
7. Execution and validation separation: syntax validity does not imply executed test pass.
"""

import re
import pytest

from backend.app.prompt.format_rules import detect_explicit_format_requirements
from backend.app.prompt.prompt_builder import PromptBuilder
from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.docker_runtime import DockerRuntime
from backend.app.sandbox.languages.python_runner import PythonRunner, is_python_ml_code
from backend.app.sandbox.sandbox_runner import ExecutionRequest, SandboxRunner
from backend.app.sandbox.schemas import ExecutionStatus, SandboxResult
from backend.app.validation.validators import PythonValidator
from backend.app.validation.schemas import ValidationStatus


# ---------------------------------------------------------------------------
# Test 1: Dynamic Image and Resource Profile Selection
# ---------------------------------------------------------------------------


def test_standard_python_selects_default_image_and_limits():
    """Verify non-ML Python code uses minimal image and standard 256MB / 3s limits."""
    runner = PythonRunner()
    config = SandboxConfig()

    code = "def add(a, b):\n    return a + b\n\nprint(add(2, 3))\n"
    assert is_python_ml_code(code) is False

    plan = runner.build_plan(code, config)
    assert plan.image_tag == "bhasha2code-sandbox-python:1.0.0"
    assert plan.is_ml is False
    assert plan.timeout_seconds == 3.0
    assert plan.memory_limit_mb == 256


@pytest.mark.parametrize(
    "import_stmt",
    [
        "import sklearn",
        "from sklearn.pipeline import Pipeline",
        "from sklearn.feature_extraction.text import TfidfVectorizer",
        "import numpy as np",
        "import pandas as pd",
        "from scipy import stats",
    ],
)
def test_ml_python_selects_ml_image_and_expanded_profile(import_stmt: str):
    """Verify scientific and ML imports select python-ml image and 768MB / 10s limits."""
    runner = PythonRunner()
    config = SandboxConfig()

    code = f"{import_stmt}\n\nprint('ML initialized')\n"
    assert is_python_ml_code(code) is True

    plan = runner.build_plan(code, config)
    assert plan.image_tag == "bhasha2code-sandbox-python-ml:1.0.0"
    assert plan.is_ml is True
    assert plan.timeout_seconds == 10.0
    assert plan.memory_limit_mb == 768


# ---------------------------------------------------------------------------
# Test 2: PromptBuilder ML Directives and Invariants
# ---------------------------------------------------------------------------


def test_ml_prompt_builder_distinguishes_features_from_labels():
    """Verify prompt builder instructs separating X from y and passing raw text to Pipeline."""
    builder = PromptBuilder()
    prompt = "Create a TF-IDF and Logistic Regression sentiment classification model with exactly 12 samples."

    req = detect_explicit_format_requirements(prompt)
    assert req.num_samples == 12

    spec = builder.build(user_message=prompt)

    # 1. Feature / label separation
    assert any(
        "Input features (X) and target labels (y) MUST be strictly separated" in c
        for c in spec.explicit_constraints
    )

    # 2. Raw text pipeline inputs (no pre-transform)
    assert any(
        "pass a 1D list of raw text strings directly to pipeline.fit(X, y)" in c
        for c in spec.explicit_constraints
    )
    assert any(
        "NEVER pre-transform X with TF-IDF" in c
        for c in spec.explicit_constraints
    )

    # 3. Predict format
    assert any(
        "pipeline.predict() MUST take a 1D list of raw strings" in c
        for c in spec.explicit_constraints
    )

    # 4. Dataset size requirement
    assert any("exactly 12 training samples in X" in c for c in spec.explicit_constraints)
    assert any("len(X) == len(y) == 12" in c for c in spec.explicit_constraints)


def test_multilingual_ml_sample_count_detection():
    """Verify multilingual dataset size detection in Marathi and Hindi."""
    hindi_prompt = "Mujhe TF-IDF classifier ke liye barah samples do"
    req_hi = detect_explicit_format_requirements(hindi_prompt)
    assert req_hi.num_samples == 12

    marathi_prompt = "Sentiment classification sathi bara samples cha dataset banwa"
    req_mr = detect_explicit_format_requirements(marathi_prompt)
    assert req_mr.num_samples == 12


# ---------------------------------------------------------------------------
# Test 3: Sandbox Error Classification Distinction
# ---------------------------------------------------------------------------


def test_missing_dependency_distinguished_from_syntax_and_runtime_error():
    """Verify missing package produces DEPENDENCY_ERROR status and clear diagnostic."""
    runner = SandboxRunner()
    if not runner.is_available():
        pytest.skip("Docker daemon unavailable")

    missing_code = "import nonexistent_package_xyz\nprint('Done')\n"
    res = runner.execute_code(language="python", code=missing_code)

    assert res.status == ExecutionStatus.DEPENDENCY_ERROR
    assert any("[DEPENDENCY_ERROR]" in d for d in res.diagnostics)
    assert any("nonexistent_package_xyz" in d for d in res.diagnostics)


def test_syntax_error_rejected_at_validation_gate():
    """Verify syntax errors fail at T18 validation before entering Docker container."""
    runner = SandboxRunner()

    syntax_bad_code = "def bad_syntax(:\n    pass\n"
    res = runner.execute_code(language="python", code=syntax_bad_code)

    assert res.status == ExecutionStatus.VALIDATION_FAILED
    assert any("ERROR" in d for d in res.diagnostics)


def test_runtime_error_distinguished_from_dependency_error():
    """Verify arithmetic runtime exceptions remain RUNTIME_ERROR."""
    runner = SandboxRunner()
    if not runner.is_available():
        pytest.skip("Docker daemon unavailable")

    div_zero_code = "x = 10 / 0\n"
    res = runner.execute_code(language="python", code=div_zero_code)

    assert res.status == ExecutionStatus.RUNTIME_ERROR
    assert res.exit_code == 1


# ---------------------------------------------------------------------------
# Test 4: Container Execution & Pipeline Verification in Isolated Sandbox
# ---------------------------------------------------------------------------


def test_ml_sandbox_imports_and_pipeline_execution():
    """Execute complete TF-IDF + LogisticRegression pipeline in isolated sandbox."""
    runner = SandboxRunner()
    if not runner.is_available():
        pytest.skip("Docker daemon unavailable")

    ml_code = (
        "import sklearn\n"
        "import numpy as np\n"
        "import pandas as pd\n"
        "import scipy\n"
        "from sklearn.feature_extraction.text import TfidfVectorizer\n"
        "from sklearn.linear_model import LogisticRegression\n"
        "from sklearn.pipeline import Pipeline\n\n"
        "# Exactly 12 balanced samples\n"
        "X_train = [\n"
        "    'I absolutely love this amazing product',\n"
        "    'Outstanding customer support and great experience',\n"
        "    'Best purchase I have ever made, highly recommended',\n"
        "    'Truly fantastic and works like a charm',\n"
        "    'Delighted with the super fast delivery',\n"
        "    'Very good quality and extremely helpful',\n"
        "    'Terrible service and completely broken',\n"
        "    'Horrible experience, I want my money back',\n"
        "    'Worst item ever received, completely defective',\n"
        "    'Awful support and very rude staff',\n"
        "    'Disappointed with the poor build quality',\n"
        "    'Waste of money, do not buy this'\n"
        "]\n"
        "y_train = [\n"
        "    'positive', 'positive', 'positive', 'positive', 'positive', 'positive',\n"
        "    'negative', 'negative', 'negative', 'negative', 'negative', 'negative'\n"
        "]\n\n"
        "assert len(X_train) == 12\n"
        "assert len(y_train) == 12\n\n"
        "# Pipeline takes raw text directly into TfidfVectorizer\n"
        "pipeline = Pipeline([\n"
        "    ('tfidf', TfidfVectorizer()),\n"
        "    ('clf', LogisticRegression())\n"
        "])\n"
        "pipeline.fit(X_train, y_train)\n\n"
        "# Predictions pass 1D list of raw strings\n"
        "test_samples = ['love this product', 'worst and awful service']\n"
        "predictions = pipeline.predict(test_samples)\n"
        "assert predictions[0] == 'positive', f'Expected positive, got {predictions[0]}'\n"
        "assert predictions[1] == 'negative', f'Expected negative, got {predictions[1]}'\n"
        "print(f'Trained on {len(X_train)} samples. Predictions: {list(predictions)}')\n"
    )

    result = runner.execute_code(language="python", code=ml_code)

    assert result.status == ExecutionStatus.SUCCESS
    assert result.exit_code == 0
    assert "Trained on 12 samples." in result.stdout
    assert "positive" in result.stdout
    assert "negative" in result.stdout


# ---------------------------------------------------------------------------
# Test 5: Sandbox Security Invariants
# ---------------------------------------------------------------------------


def test_sandbox_security_flags_on_ml_plan():
    """Verify secure Docker arguments: non-root user, read-only rootfs, no network."""
    runtime = DockerRuntime()
    runner = PythonRunner()
    code = "import sklearn\nprint('ok')"
    plan = runner.build_plan(code, runtime.config)

    args = runtime.build_docker_run_args(plan, "test-vol", "test-cid")

    assert "--network" in args
    net_idx = args.index("--network")
    assert args[net_idx + 1] == "none"

    assert "--cap-drop" in args
    cap_idx = args.index("--cap-drop")
    assert args[cap_idx + 1] == "ALL"

    assert "--read-only" in args
    assert "--user" in args
    user_idx = args.index("--user")
    assert args[user_idx + 1] == "1000:1000"

    assert plan.image_tag == "bhasha2code-sandbox-python-ml:1.0.0"
    assert "bhasha2code-sandbox-python-ml:1.0.0" in args
    # Memory limit for ML must be 768m
    assert "--memory" in args
    mem_idx = args.index("--memory")
    assert args[mem_idx + 1] == "768m"


# ---------------------------------------------------------------------------
# Test 6: Prompt & AST ML Consistency Regression Tests
# ---------------------------------------------------------------------------


def test_final_rendered_prompt_contains_ml_policy_and_invariants():
    """Verify that ML instructions are present in the final rendered prompt delivered to LLM."""
    builder = PromptBuilder()
    prompt = (
        "Write complete Python code using scikit-learn for sentiment classification with exactly 12 samples "
        "(positive/negative). Include 2 test cases with assertions. Give only complete code."
    )
    spec = builder.build(user_message=prompt)

    # 1. PromptSpecification contains ml_instruction
    assert spec.ml_instruction is not None
    assert "MACHINE LEARNING SPECIFICATION & PIPELINE INVARIANTS" in spec.ml_instruction

    # 2. Rendered text contains dedicated ML section
    rendered = spec.render()
    assert "=== MACHINE LEARNING SPECIFICATION & PIPELINE INVARIANTS ===" in rendered
    assert "Strictly Distinguish Features (X) and Target Labels (y)" in rendered
    assert "Pass a 1D list of raw text strings directly to pipeline.fit" in rendered
    assert "EXACT DATASET SIZE REQUIREMENT: You MUST generate exactly 12 samples in X and exactly 12 corresponding target labels in y" in rendered
    assert "SENTIMENT TARGET LABELS REQUIREMENT: Use explicit 'positive' and 'negative' string labels for y" in rendered

    # 3. Directives section at the bottom also enforces ML invariants
    assert "=== CODE PRESERVATION & SECURITY DIRECTIVES ===" in rendered
    assert "- MACHINE LEARNING PIPELINE & TARGET INVARIANTS:" in rendered
    assert "X (features) must be raw text strings. y (target) must be ground-truth class labels" in rendered

    # 4. Safe ML summary hook
    summary = spec.get_ml_policy_summary()
    assert summary["has_ml_policy"] is True
    assert "distinguish_features_and_target" in summary["ml_invariants"]
    assert "raw_text_pipeline_inputs" in summary["ml_invariants"]
    assert prompt not in str(summary)  # Does not leak private prompt text


def test_continuation_detection_does_not_falsely_trigger_on_complete_code():
    """Verify demanding 'complete code' does NOT misclassify fresh requests as truncated continuations."""
    builder = PromptBuilder()
    prompt = "Give only complete code and two simple test cases for sentiment classification."
    spec = builder.build(user_message=prompt)

    assert not any("CONTINUATION TASK" in c for c in spec.explicit_constraints)
    assert any("USER DEMAND: Output ONLY complete working code" in c for c in spec.explicit_constraints)


def test_ast_validator_catches_duplicate_vectorization():
    """Verify AST validator detects passing pre-vectorized X into a Pipeline that has TfidfVectorizer."""
    validator = PythonValidator()
    code = (
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.feature_extraction.text import TfidfVectorizer\n"
        "from sklearn.linear_model import LogisticRegression\n\n"
        "texts = ['good', 'bad']\n"
        "labels = ['pos', 'neg']\n"
        "vec = TfidfVectorizer()\n"
        "X = vec.fit_transform(texts)\n"
        "pipeline = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LogisticRegression())])\n"
        "pipeline.fit(X, labels)\n"
    )
    result = validator.validate(code)
    assert result.status == ValidationStatus.INVALID
    assert any("Duplicate text vectorization" in d.message for d in result.diagnostics)


def test_ast_validator_catches_target_identical_to_input_text():
    """Verify AST validator detects fitting pipeline to predict input text instead of labels."""
    validator = PythonValidator()
    code = (
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.feature_extraction.text import TfidfVectorizer\n"
        "from sklearn.linear_model import LogisticRegression\n\n"
        "texts = ['good', 'bad']\n"
        "pipeline = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LogisticRegression())])\n"
        "pipeline.fit(texts, texts)\n"
    )
    result = validator.validate(code)
    assert result.status == ValidationStatus.INVALID
    assert any("Target labels y cannot be identical" in d.message for d in result.diagnostics)


def test_ast_validator_catches_nested_2d_list_in_predict():
    """Verify AST validator detects passing [['text']] instead of ['text'] to predict()."""
    validator = PythonValidator()
    code = (
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.feature_extraction.text import TfidfVectorizer\n"
        "from sklearn.linear_model import LogisticRegression\n\n"
        "texts = ['good', 'bad']\n"
        "labels = ['pos', 'neg']\n"
        "pipeline = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LogisticRegression())])\n"
        "pipeline.fit(texts, labels)\n"
        "res = pipeline.predict([['sample text']])\n"
    )
    result = validator.validate(code)
    assert result.status == ValidationStatus.INVALID
    assert any("nested 2D list of text" in d.message for d in result.diagnostics)


def test_ast_validator_catches_mismatched_sample_counts():
    """Verify AST validator detects discrepancy between feature samples and target label counts."""
    validator = PythonValidator()
    code = (
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.feature_extraction.text import TfidfVectorizer\n"
        "from sklearn.linear_model import LogisticRegression\n\n"
        "texts = ['1', '2', '3']\n"
        "labels = ['pos', 'neg']\n"
        "pipeline = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LogisticRegression())])\n"
        "pipeline.fit(texts, labels)\n"
    )
    result = validator.validate(code)
    assert result.status == ValidationStatus.INVALID
    assert any("Inconsistent sample count" in d.message for d in result.diagnostics)


def test_ast_validator_catches_numeric_assertions_on_string_labels():
    """Verify AST validator flags assertions checking == 1 or == 0 when trained on string labels."""
    validator = PythonValidator()
    code = (
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.feature_extraction.text import TfidfVectorizer\n"
        "from sklearn.linear_model import LogisticRegression\n\n"
        "texts = ['good product', 'bad service']\n"
        "labels = ['positive', 'negative']\n"
        "pipeline = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LogisticRegression())])\n"
        "pipeline.fit(texts, labels)\n"
        "pred = pipeline.predict(['good product'])\n"
        "assert pred == 1\n"
    )
    result = validator.validate(code)
    assert result.status == ValidationStatus.INVALID
    assert any("Assertion compares text model prediction with numeric literal" in d.message for d in result.diagnostics)


def test_ast_validator_passes_valid_12_sample_sentiment_pipeline():
    """Verify valid 12-sample text classification pipeline passes AST validation with zero errors."""
    validator = PythonValidator()
    code = (
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.feature_extraction.text import TfidfVectorizer\n"
        "from sklearn.linear_model import LogisticRegression\n\n"
        "X_train = [\n"
        "    'I loved the exceptional customer service',\n"
        "    'Fantastic quality, exceeded expectations',\n"
        "    'Best purchase I have made this year',\n"
        "    'Works wonderfully and arrived quickly',\n"
        "    'Highly recommended for everyone',\n"
        "    'Great product with very intuitive design',\n"
        "    'Terrible customer support, very rude',\n"
        "    'Defective item stopped working in a day',\n"
        "    'Completely dissatisfied with the purchase',\n"
        "    'Extremely overpriced for such poor results',\n"
        "    'Disappointed with the poor build quality',\n"
        "    'Waste of money, do not buy this'\n"
        "]\n"
        "y_train = [\n"
        "    'positive', 'positive', 'positive', 'positive', 'positive', 'positive',\n"
        "    'negative', 'negative', 'negative', 'negative', 'negative', 'negative'\n"
        "]\n\n"
        "pipeline = Pipeline([\n"
        "    ('tfidf', TfidfVectorizer()),\n"
        "    ('clf', LogisticRegression())\n"
        "])\n"
        "pipeline.fit(X_train, y_train)\n"
        "pred = pipeline.predict(['loved this purchase'])\n"
        "assert pred[0] in ['positive', 'negative']\n"
    )
    result = validator.validate(code)
    assert result.status == ValidationStatus.VALID
    assert len(result.diagnostics) == 0

