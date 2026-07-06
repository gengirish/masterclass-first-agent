"""Pre-deploy checks — run before `fly deploy` or in CI.

    uv run python -m scripts.preflight

Exits 0 when the repo is ready to ship; 1 otherwise.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
CHROMA_DIR = ROOT / ".chroma"
DATA_DIR = ROOT / "data"
REQUIRED_SECRET_VARS = ("OPENROUTER_API_KEY",)


def check(name: str, ok: bool, detail: str) -> bool:
    mark = "ok" if ok else "FAIL"
    print(f"  [{mark}] {name}: {detail}")
    return ok


def main() -> int:
    ci_mode = os.environ.get("CI") == "true" or "--ci" in sys.argv
    print("Preflight checks" + (" (CI mode)" if ci_mode else "") + "\n")
    ok = True

    ok &= check(
        "data/",
        DATA_DIR.is_dir() and any(DATA_DIR.iterdir()),
        f"{len(list(DATA_DIR.glob('*')))} file(s) under {DATA_DIR}",
    )

    chroma_exists = CHROMA_DIR.is_dir()
    if ci_mode:
        ok &= check(".chroma/", True, "skipped in CI")
    else:
        ok &= check(
            ".chroma/",
            chroma_exists,
            "present — run `uv run python -m scripts.ingest` if missing",
        )

        if chroma_exists:
            try:
                import chromadb

                client = chromadb.PersistentClient(path=str(CHROMA_DIR))
                collection = client.get_collection("intelliforge-docs")
                count = collection.count()
                ok &= check(
                    "chroma collection",
                    count > 0,
                    f"intelliforge-docs has {count} chunk(s)",
                )
            except Exception as exc:
                ok &= check("chroma collection", False, str(exc))

    if ci_mode:
        ok &= check("LLM API key", True, "skipped in CI")
    else:
        key_set = any(os.environ.get(v) for v in REQUIRED_SECRET_VARS) or os.environ.get(
            "OPENAI_API_KEY"
        )
        ok &= check(
            "LLM API key",
            bool(key_set),
            "OPENROUTER_API_KEY or OPENAI_API_KEY in .env / Fly secrets",
        )

    web_lock = ROOT / "web" / "package-lock.json"
    ok &= check("web/package-lock.json", web_lock.is_file(), "npm lockfile present")

    print()
    if ok:
        print("All preflight checks passed.")
        return 0
    print("Preflight failed — fix the items above before deploying.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
