#!/usr/bin/env bash
# Ingest FAQ into Chroma, then deploy — embeddings are baked into the image
# before any machine serves /ask.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> Ingesting data/ into Chroma..."
uv run python -m scripts.ingest

echo "==> Deploying to Fly.io..."
fly deploy "$@"
