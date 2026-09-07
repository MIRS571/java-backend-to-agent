"""HTTP request and response contracts for the Agent API."""

from pydantic import BaseModel, ConfigDict, field_validator


class ChatRequest(BaseModel):
    """Validated input accepted from a trusted Java backend."""

    model_config = ConfigDict(extra="forbid")

    user_id: str
    thread_id: str
    message: str

    @field_validator("user_id", "thread_id", "message")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("字段不能只包含空格")
        return cleaned_value


class ChatResponse(BaseModel):
    """Stable non-streaming response returned by the API."""

    thread_id: str
    answer: str
