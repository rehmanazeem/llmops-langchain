"""LLM access behind a small Protocol so tests can inject a fake."""
from typing import Protocol

from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM

from llmops.config import Settings


class TextGenerator(Protocol):
    """Anything that turns a prompt into a completion string."""

    def generate(self, prompt: str) -> str: ...


class OllamaGenerator:
    """``OllamaLLM | StrOutputParser`` chain against a local Ollama server."""

    def __init__(self, settings: Settings):
        self._chain = (
            OllamaLLM(base_url=settings.ollama_base_url, model=settings.model)
            | StrOutputParser()
        )

    def generate(self, prompt: str) -> str:
        return self._chain.invoke(prompt)
