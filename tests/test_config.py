import pytest

from java_backend_to_agent.config import ModelSettings


def test_settings_report_only_missing_variable_names(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("LLM_MODEL", "test-model")
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.setenv("LLM_BASE_URL", "https://provider.invalid/v1")

    settings = ModelSettings.from_env(load_file=False)

    assert settings.missing_variables() == ("LLM_API_KEY",)


def test_require_complete_does_not_include_configured_values():
    settings = ModelSettings(
        model="private-model-name",
        api_key="private-key",
        base_url="https://private-provider.invalid/v1",
    )

    assert settings.require_complete() is settings


def test_missing_error_contains_names_not_secrets():
    settings = ModelSettings(
        model="private-model-name",
        api_key="",
        base_url="",
    )

    with pytest.raises(RuntimeError) as exc_info:
        settings.require_complete()

    message = str(exc_info.value)
    assert "LLM_API_KEY" in message
    assert "LLM_BASE_URL" in message
    assert "private-model-name" not in message
