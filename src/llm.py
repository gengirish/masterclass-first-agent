"""Multi-provider LLM helper.

The masterclass agent uses the OpenAI Python SDK for both chat and
embeddings. Every modern LLM provider worth caring about (OpenRouter,
Groq, NVIDIA NIM, OpenAI itself, ...) exposes an OpenAI-compatible
endpoint, so we can support all of them by swapping `base_url` and the
api key at client construction time.

This module wraps that swap behind two slug-aware helpers:

    from .llm import make_client, model_name, embed

    client = make_client(MODEL)
    response = client.chat.completions.create(
        model=model_name(MODEL),
        messages=[...],
    )

Provider-prefix syntax for `MODEL` and `EMBED_MODEL` env vars:

    openai/gpt-4o-mini                   <- bare slug, uses default provider
    openrouter:openai/gpt-4o-mini        <- explicit
    groq:llama-3.3-70b-versatile
    nim:meta/llama-3.3-70b-instruct
    nim:nvidia/nv-embedqa-e5-v5
    openai:gpt-4o-mini

The default provider is set by the `LLM_DEFAULT_PROVIDER` env var
(defaults to ``openrouter``).
"""
from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

# provider name -> (base_url, env var holding api key)
_PROVIDERS: dict[str, tuple[str, str]] = {
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
    "nim": ("https://integrate.api.nvidia.com/v1", "NIM_API_KEY"),
    "openai": ("https://api.openai.com/v1", "OPENAI_API_KEY"),
}


def _split(slug: str) -> tuple[str, str]:
    """Parse a `provider:model` slug. Falls back to LLM_DEFAULT_PROVIDER."""
    default = os.environ.get("LLM_DEFAULT_PROVIDER", "openrouter")
    if ":" in slug:
        head, rest = slug.split(":", 1)
        if head in _PROVIDERS:
            return head, rest
    return default, slug


def model_name(slug: str) -> str:
    """Return the bare model id (without any `provider:` prefix)."""
    return _split(slug)[1]


def provider_for(slug: str) -> str:
    """Return the provider name resolved from a model slug."""
    return _split(slug)[0]


def make_client(slug: str) -> OpenAI:
    """Build an OpenAI-compatible client routed at the right provider."""
    provider, _ = _split(slug)
    base_url, key_var = _PROVIDERS[provider]
    api_key = os.environ.get(key_var) or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            f"No API key for provider '{provider}'. "
            f"Set {key_var} (or OPENAI_API_KEY as a fallback) in your .env."
        )
    return OpenAI(api_key=api_key, base_url=base_url)


def embed(
    client: OpenAI,
    slug: str,
    texts: list[str],
    *,
    kind: str = "passage",
) -> list[list[float]]:
    """Run an embeddings call, handling provider-specific quirks.

    `kind` should be ``"passage"`` for documents being indexed and
    ``"query"`` for the query text used at search time. NVIDIA NIM
    requires this distinction; other providers ignore it.
    """
    provider, model = _split(slug)
    kwargs: dict[str, Any] = {"model": model, "input": texts}
    if provider == "nim":
        kwargs["extra_body"] = {"input_type": "query" if kind == "query" else "passage"}
    response = client.embeddings.create(**kwargs)
    return [item.embedding for item in response.data]
