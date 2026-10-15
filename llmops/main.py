"""Application factory."""
from typing import Optional

from fastapi import FastAPI

from llmops.chain import OllamaGenerator, TextGenerator
from llmops.config import Settings, apply_tracing_defaults
from llmops.routes import build_router


def create_app(generator: Optional[TextGenerator] = None) -> FastAPI:
    """Build the app. Pass ``generator`` to inject a fake (tests); by default
    an Ollama-backed generator is created per request from env settings."""
    apply_tracing_defaults()
    app = FastAPI()
    get_generator = (lambda: generator) if generator else (
        lambda: OllamaGenerator(Settings.from_env())
    )
    app.include_router(build_router(get_generator))
    return app
