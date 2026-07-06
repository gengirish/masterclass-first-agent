# Ingest FAQ into Chroma, then deploy — embeddings are baked into the image
# before any machine serves /ask.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "==> Ingesting data/ into Chroma..."
uv run python -m scripts.ingest

Write-Host "==> Deploying to Fly.io..."
fly deploy @args
