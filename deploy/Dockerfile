FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
# uv.lock is included if you run `uv sync` locally first; uncomment if present.
# COPY uv.lock ./

RUN uv sync --no-dev

COPY src ./src
COPY scripts ./scripts
COPY data ./data

ENV PORT=8080
EXPOSE 8080

CMD ["uv", "run", "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080"]
