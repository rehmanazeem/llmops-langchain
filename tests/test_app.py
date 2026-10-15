from fastapi.testclient import TestClient

from llmops import create_app
from llmops.config import Settings


class FakeGenerator:
    def generate(self, prompt: str) -> str:
        return f"echo:{prompt}"


class BrokenGenerator:
    def generate(self, prompt: str) -> str:
        raise RuntimeError("ollama down")


def test_generate_returns_response():
    r = TestClient(create_app(FakeGenerator())).get("/generate", params={"prompt": "hi"})
    assert r.status_code == 200 and r.json() == {"response": "echo:hi"}


def test_generate_error_is_500():
    r = TestClient(create_app(BrokenGenerator())).get("/generate", params={"prompt": "hi"})
    assert r.status_code == 500 and r.json()["detail"] == "ollama down"


def test_missing_prompt_is_422():
    assert TestClient(create_app(FakeGenerator())).get("/generate").status_code == 422


def test_settings_from_env(monkeypatch):
    assert Settings.from_env().model == "llama3.2"
    monkeypatch.setenv("OLLAMA_MODEL", "other")
    assert Settings.from_env().model == "other"
