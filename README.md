# llmops-langchain

> A FastAPI + LangChain + Ollama service demonstrating LLMOps patterns, with LangSmith tracing and accompanying RAG / multimodal notebooks.

## Overview

This repository showcases how to build and operate local LLM applications using
the LangChain ecosystem with **locally-served models via [Ollama](https://ollama.com)**
and **observability via [LangSmith](https://smith.langchain.com)**.

It contains two complementary parts:

1. **A deployable FastAPI service** (`app.py`) that exposes a text-generation
   endpoint backed by an Ollama-served model (`llama3.2`), wired through a
   LangChain runnable chain and traced with LangSmith. A `Dockerfile` is
   included to containerize it.
2. **Exploratory Jupyter notebooks** that demonstrate a Retrieval-Augmented
   Generation (RAG) pipeline over PDFs using a Qdrant vector store and Ollama
   embeddings, plus a multimodal (image + text) assistant.

## Key Features

- **FastAPI inference endpoint** (`GET /generate`) using a LangChain
  `LLM | StrOutputParser` chain.
- **Local-first LLMs** served by Ollama (no external model API required).
- **LangSmith tracing** enabled via environment variables for run
  observability (the LLMOps angle).
- **Pluggable PDF parsing** (`py_modules/document_loader.py`) implementing the
  Strategy pattern with `PyPDFLoader` and `UnstructuredLoader` backends.
- **RAG pipeline notebooks**: chunking with `RecursiveCharacterTextSplitter`,
  embedding with `OllamaEmbeddings`, storage/retrieval in `QdrantVectorStore`,
  and prompt composition via LangChain runnables.
- **Multimodal assistant notebook** using `ChatOllama` with base64-encoded
  image inputs.
- **Containerized deployment** via the included `Dockerfile`.

## Tech Stack

| Area              | Technology                                              |
| ----------------- | ------------------------------------------------------- |
| API framework     | FastAPI, Uvicorn                                        |
| LLM orchestration | LangChain (`langchain-core`, `langchain-ollama`, etc.) |
| Local models      | Ollama (`llama3.2`)                                     |
| Observability     | LangSmith (`LANGCHAIN_TRACING_V2`)                      |
| RAG / vectors     | Qdrant (`langchain-qdrant`, `qdrant-client`)            |
| Document loading  | PyPDFLoader, UnstructuredLoader, PyMuPDF                |
| Notebooks         | Jupyter, matplotlib, Pillow                             |
| Packaging         | Docker (python:3.9-slim)                                |

## Architecture

```mermaid
flowchart LR
    Client[Client / curl] -->|GET /generate?prompt=...| API[FastAPI app.py]
    API --> Chain[LangChain chain\nOllamaLLM | StrOutputParser]
    Chain --> Ollama[(Ollama server\nlocalhost:11434\nllama3.2)]
    Chain -.traces.-> LangSmith[(LangSmith)]
    API -->|JSON response| Client

    subgraph Notebooks[RAG / Multimodal notebooks]
        PDFs[PDFs] --> Loader[DocumentLoader\nPyPDF / Unstructured]
        Loader --> Splitter[RecursiveCharacterTextSplitter]
        Splitter --> Embed[OllamaEmbeddings]
        Embed --> Qdrant[(Qdrant Vector Store)]
        Qdrant --> Retrieve[Retriever + Prompt + OllamaLLM]
    end
```

## Setup

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com) installed and running locally, with the model pulled:
  ```bash
  ollama pull llama3.2
  ```
  Ollama listens on `http://localhost:11434` by default.
- A [LangSmith](https://smith.langchain.com) account and API key (for tracing).

### Install

```bash
git clone https://github.com/<your-username>/llmops-langchain.git
cd llmops-langchain

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Environment variables

The service reads LangSmith configuration from environment variables. Copy the
example file and fill in your own values:

```bash
cp .env.example .env
```

Required variable names:

| Variable               | Purpose                                          |
| ---------------------- | ------------------------------------------------ |
| `LANGCHAIN_API_KEY`    | Your LangSmith API key                           |
| `LANGCHAIN_TRACING_V2` | Set to `true` to enable tracing                  |
| `LANGCHAIN_ENDPOINT`   | LangSmith endpoint (`https://api.smith.langchain.com`) |
| `LANGCHAIN_PROJECT`    | Project name traces are grouped under            |

> **Note:** The current `app.py` sets these values inline via `os.environ`.
> For real deployments, load them from the environment / `.env` instead of
> hardcoding them (see *Limitations / next steps*).

## Run

### Locally

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### With Docker

```bash
docker build -t llmops-langchain .
docker run -p 8000:8000 llmops-langchain
```

> When running in Docker, `localhost:11434` refers to the container, not the
> host. Point the app at a reachable Ollama instance (e.g.
> `http://host.docker.internal:11434`) or run Ollama in a networked container.

## Usage

Once the server is running, call the `/generate` endpoint with a `prompt`
query parameter:

```bash
curl "http://localhost:8000/generate?prompt=Explain%20what%20LLMOps%20means%20in%20one%20sentence."
```

Example response:

```json
{
  "response": "LLMOps is the set of practices for deploying, monitoring, and maintaining large language model applications in production."
}
```

Interactive API docs (Swagger UI) are available at
`http://localhost:8000/docs`.

### Notebooks

The RAG and multimodal workflows live in:

- `rag_assistant.ipynb` — RAG over PDFs (with image extraction).
- `rag_assistant_noImage.ipynb` — RAG over PDFs (text only).
- `multimodel-assistant.ipynb` — multimodal (image + text) prompting.

Open them with Jupyter and run the cells top to bottom. They expect Ollama
(with the relevant models/embeddings pulled) and, for RAG, a running Qdrant
instance. Sample input data is under `DataFiles/`.

## Limitations / Next Steps

- **Secrets are hardcoded in `app.py`** (LangSmith API key and project config).
  These should be moved to environment variables / `.env` and the existing key
  rotated. See `.env.example`.
- The `/generate` endpoint uses a fixed model (`llama3.2`) and has no prompt
  templating, streaming, or input validation beyond FastAPI defaults.
- No automated tests or CI are included yet.
- The notebooks are exploratory and not packaged as reusable modules or
  endpoints.
- Docker networking to a host-run Ollama needs manual configuration (see *Run*).
- The RAG pipeline assumes a manually provisioned Qdrant collection; setup is
  not yet automated.
