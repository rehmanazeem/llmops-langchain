"""Settings read from the environment. ``LANGCHAIN_API_KEY`` is never read here."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Service settings. Defaults match the original hard-wired values."""

    model: str = "llama3.2"
    ollama_base_url: str = "http://localhost:11434"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model=os.getenv("OLLAMA_MODEL", cls.model),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", cls.ollama_base_url),
        )


def apply_tracing_defaults() -> None:
    """Set LangSmith defaults if unset. The API key must come from the
    environment (``LANGCHAIN_API_KEY``) and is never set here."""
    os.environ.setdefault("LANGCHAIN_PROJECT", "Docker-APP")
    os.environ.setdefault("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
