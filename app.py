import os
from fastapi import FastAPI, HTTPException
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM


# Set LANGCHAIN_API_KEY in your environment before running — never hardcode it.
os.environ.setdefault("LANGCHAIN_PROJECT", "Docker-APP")
os.environ.setdefault("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")

app = FastAPI()

# LangChain LLM Wrapper
class CustomOllama(OllamaLLM):
    """Thin wrapper around ``OllamaLLM`` pinned to the local Ollama server."""

    def __init__(self, model: str):
        super().__init__(endpoint="http://localhost:11434", model=model)


@app.get("/generate")
async def generate(prompt: str):
    """Generate a completion for ``prompt`` using the local Ollama model and
    return it as JSON. Raises HTTP 500 on any inference error."""
    try:
        llm = CustomOllama(model="llama3.2")
        output_parser = StrOutputParser()
        chain = llm | output_parser
        
        response = chain.invoke(prompt)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
