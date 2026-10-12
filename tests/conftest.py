import os
import pytest

# Ensure testing environment does not inherit local development .env overrides
os.environ.pop("OLLAMA_MODEL", None)
os.environ.pop("OLLAMA_NUM_PREDICT", None)

@pytest.fixture(autouse=True)
def isolate_test_environment(monkeypatch):
    """Ensure tests run with standard configuration defaults."""
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    monkeypatch.delenv("OLLAMA_NUM_PREDICT", raising=False)
