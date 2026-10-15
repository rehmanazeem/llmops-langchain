"""HTTP routes."""
from typing import Callable

from fastapi import APIRouter, HTTPException

from llmops.chain import TextGenerator


def build_router(get_generator: Callable[[], TextGenerator]) -> APIRouter:
    """Routes that obtain their generator lazily per request (as the original
    app built its LLM per request), so startup never needs Ollama."""
    router = APIRouter()

    @router.get("/generate")
    async def generate(prompt: str):
        """Generate a completion for ``prompt`` and return it as JSON.
        Raises HTTP 500 on any inference error."""
        try:
            return {"response": get_generator().generate(prompt)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
