# Masterclass: Build Your First AI Agent in 3 Hours

Starter repo for the **IntelliForge "Build Your First AI Agent in 3 Hours"** masterclass.

By the end of the masterclass you will have:

1. A tool-using AI agent (calculator + web search stub)
2. A RAG layer over a sample PDF using ChromaDB
3. A FastAPI server wrapping the agent
4. The agent deployed to a public URL on Fly.io

---

## Prerequisites

- **Python 3.11+** ([python.org](https://python.org))
- **uv** (`pip install uv`) — fast Python package manager
- **Git**
- **OpenAI API key** ([platform.openai.com](https://platform.openai.com)) with a small budget cap (~$5)
- **GitHub account**
- **Fly.io account** + Fly CLI (for the deploy step)

You should be comfortable reading a `for` loop and running a Python script. This is *not* a beginner Python class.

---

## Quick start (3 commands)

```bash
git clone https://github.com/gengirish/masterclass-first-agent
cd masterclass-first-agent
uv sync
```

Then create your env file and paste your OpenAI key:

```bash
cp .env.example .env
# open .env in your editor, replace `sk-...replace-me...` with your real key
```

Smoke test (should print a model id):

```bash
uv run python -c "from openai import OpenAI; print(OpenAI().models.list().data[0].id)"
```

---

## Project layout

```
masterclass-first-agent/
|-- pyproject.toml           # uv-managed project + dependencies
|-- .env.example             # template for your OPENAI_API_KEY
|-- README.md                # this file
|-- data/
|   `-- intelliforge-faq.md  # sample doc for the RAG layer
|-- src/
|   |-- __init__.py
|   |-- agent_v0_chatbot.py  # FILLED  - baseline chatbot, no tools
|   |-- agent_v1_tools.py    # SKELETON - Hour 2 Step 1 (tool calling + memory)
|   |-- agent_v2_rag.py      # SKELETON - Hour 2 Step 2 (RAG over docs)
|   |-- tools.py             # FILLED  - calculator, web_search, search_docs
|   `-- server.py            # SKELETON - FastAPI server for deploy
|-- reference/
|   `-- solutions/           # complete working versions of each skeleton
|       |-- agent_v1_tools.py
|       |-- agent_v2_rag.py
|       `-- server.py
|-- scripts/
|   `-- ingest.py            # one-shot: read data/ -> embed -> Chroma
`-- deploy/
    |-- Dockerfile
    `-- fly.toml
```

The **SKELETON** files have function signatures and `# TODO` comments at every place you type during the live session. You never start from a blank file.

If you get stuck or are running through this on your own, peek at the matching file under `reference/solutions/` for a working implementation.

---

## How to run each step

### Step 0 - baseline chatbot (no tools, no memory of "memory")

```bash
uv run python -m src.agent_v0_chatbot "Hello, who are you?"
```

This is the "before" picture. Confirms your API key works.

### Step 1 - tool-calling agent

Fill in the `# TODO` blocks in `src/agent_v1_tools.py`, then run:

```bash
uv run python -m src.agent_v1_tools "What is 17% of 4,829?"
```

You should see iteration logs and a final answer that used the calculator tool.

### Step 2 - RAG-augmented agent

First ingest the sample doc into ChromaDB:

```bash
uv run python -m scripts.ingest
```

Then ask a doc-grounded question:

```bash
uv run python -m src.agent_v2_rag "How long is the IntelliForge bootcamp and what does it cost?"
```

The agent should call `search_docs`, retrieve the relevant chunk(s), and answer with a citation.

### Step 3 - run the FastAPI server locally

```bash
uv run uvicorn src.server:app --reload
```

In a second terminal:

```bash
curl -X POST http://localhost:8000/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What does the bootcamp cost?\"}"
```

(On macOS / Linux / WSL use single quotes around the JSON.)

### Step 4 - deploy to Fly.io

```bash
# 1. Install fly CLI (one-time)
#    Windows (PowerShell): iwr https://fly.io/install.ps1 -useb | iex
#    macOS / Linux:        curl -L https://fly.io/install.sh | sh

# 2. Authenticate
fly auth signup    # or: fly auth login

# 3. Set the API key as a Fly secret (don't bake it into the image)
fly secrets set OPENAI_API_KEY=<paste-your-key>

# 4. Launch + deploy
fly launch --copy-config --no-deploy   # pick a globally-unique app name
fly deploy
```

When `fly deploy` finishes, hit your public URL:

```bash
curl https://<your-app-name>.fly.dev/
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `openai.AuthenticationError` 401 | API key in `.env` is missing or wrong. Re-paste, save, re-run. |
| `ModuleNotFoundError: chromadb` | `uv sync` did not finish. Re-run it. On Windows, use Python 3.11 (not 3.13 yet). |
| ChromaDB SQLite errors on Windows | Delete the `.chroma/` folder and re-run `python -m scripts.ingest`. |
| Agent runs forever / hits iteration cap | Lower `max_iterations` or simplify the question. The default cap is 6. |
| `fly deploy` fails on Windows path issues | Run inside WSL2 or use the GitHub Actions deploy variant. |
| OPENAI cost spikes | The masterclass hits ~$0.01 per attendee. Set a hard cap of $5 on your OpenAI billing dashboard. |

WhatsApp setup support: `wa.me/918555960837`.

---

## What you should NOT do in this repo

- Don't commit `.env`. It is git-ignored. If you ever do, **rotate the key immediately**.
- Don't rename module files mid-masterclass - the import paths in `server.py` and the deploy config assume the layout above.
- Don't bake `OPENAI_API_KEY` into the Dockerfile. Use `fly secrets set`.

---

## License

MIT. Use this code in your own projects, demos, portfolios, freelance work - whatever helps you ship.
