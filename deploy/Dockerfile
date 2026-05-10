FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
COPY scripts ./scripts
COPY data ./data
COPY .chroma ./.chroma

ENV PORT=8080
EXPOSE 8080

CMD [".venv/bin/uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080"]
