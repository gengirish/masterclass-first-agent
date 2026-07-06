FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    LLM_DEFAULT_PROVIDER=openrouter \
    MODEL=openai/gpt-4o-mini \
    EMBED_MODEL=openai/text-embedding-3-small

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
COPY scripts ./scripts
COPY data ./data

# Pre-built at deploy time — run `scripts/deploy-fly` before `fly deploy` so
# Chroma is indexed before the image builds; /ask never waits on ingestion.
COPY .chroma ./.chroma

ENV PORT=8080
EXPOSE 8080

CMD [".venv/bin/uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080"]
