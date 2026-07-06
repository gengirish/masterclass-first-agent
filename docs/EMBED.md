# Embed the Bootcamp Assistant on upskill.intelliforge.tech

This guide explains how to add the IntelliForge Bootcamp Assistant as a floating chat widget on [upskill.intelliforge.tech](https://upskill.intelliforge.tech/) or any other IntelliForge site.

The widget is hosted separately from the upskill site. You only need to add a script tag (or iframe) — do not rebuild the chat UI in the upskill repo.

## For AI agents and Cursor

Machine-readable integration docs ([llms.txt spec](https://llmstxt.org/)):

| File | URL | Use when |
|------|-----|----------|
| `llms.txt` | https://masterclass-first-agent.vercel.app/llms.txt | Quick index — endpoints, snippet, links |
| `llms-full.txt` | https://masterclass-first-agent.vercel.app/llms-full.txt | **Fetch this first** — full spec, CSP, API, checklist |
| `llm.txt` | https://masterclass-first-agent.vercel.app/llm.txt | Alias of `llms.txt` (compatibility) |

In Cursor on the upskill repo, point the agent at `llms-full.txt` or paste the prompt below.

## Live URLs

| Resource | URL |
|----------|-----|
| Widget loader script | https://masterclass-first-agent.vercel.app/embed.js |
| Embed panel (iframe) | https://masterclass-first-agent.vercel.app/embed |
| Agent API (called by widget) | https://masterclass-first-agent.fly.dev |
| Demo UI (full page) | https://masterclass-first-agent.vercel.app |

The widget is already configured to allow framing from `upskill.intelliforge.tech` and `*.intelliforge.tech`.

---

## Preferred approach — script tag

Add this once, site-wide, just before `</body>` (or in the root layout if the upskill site is Next.js/React):

```html
<script
  src="https://masterclass-first-agent.vercel.app/embed.js"
  data-position="bottom-right"
  defer
></script>
```

### What `embed.js` does

- Injects a fixed green chat launcher button (bottom-right by default)
- On click, opens a panel with an iframe pointing to `/embed`
- Close button inside the panel posts `intelliforge-chat-close` to collapse it
- On mobile, the panel expands to ~85vh from the bottom

### Optional attributes

| Attribute | Values | Default |
|-----------|--------|---------|
| `data-position` | `bottom-right`, `bottom-left` | `bottom-right` |
| `data-base` | Full widget origin URL | Derived from script `src` |

Example with left positioning:

```html
<script
  src="https://masterclass-first-agent.vercel.app/embed.js"
  data-position="bottom-left"
  defer
></script>
```

---

## Alternative — direct iframe

Use this only if the script tag approach will not work (e.g. strict CSP blocking third-party scripts):

```html
<iframe
  src="https://masterclass-first-agent.vercel.app/embed"
  title="IntelliForge Bootcamp Assistant"
  style="position:fixed;bottom:24px;right:24px;width:min(400px,calc(100vw - 32px));height:min(620px,calc(100dvh - 120px));border:none;border-radius:14px;z-index:9999;box-shadow:0 20px 60px rgba(0,0,0,.45)"
  allow="clipboard-write"
></iframe>
```

Prefer the script tag — it includes the launcher button and open/close behavior.

---

## Cursor prompt (paste into the upskill repo)

**Recommended:** Tell Cursor to fetch https://masterclass-first-agent.vercel.app/llms-full.txt and follow it.

Or copy the block below into Cursor while the **upskill site repo** is open:

````
Embed the IntelliForge Bootcamp Assistant chat widget on https://upskill.intelliforge.tech/

## What to embed

A pre-built floating chat widget hosted separately. Do NOT rebuild the chat UI — only wire it into this site.

| Resource | URL |
|----------|-----|
| Widget loader script | https://masterclass-first-agent.vercel.app/embed.js |
| Embed panel (iframe) | https://masterclass-first-agent.vercel.app/embed |
| Agent API (called by widget) | https://masterclass-first-agent.fly.dev |

The widget is already configured to allow framing from `upskill.intelliforge.tech` and `*.intelliforge.tech`.

## Preferred approach — script tag

Add this once, site-wide, just before `</body>` (or in the root layout if this is Next.js/React):

```html
<script
  src="https://masterclass-first-agent.vercel.app/embed.js"
  data-position="bottom-right"
  defer
></script>
```

What `embed.js` does:
- Injects a fixed green chat launcher button (bottom-right by default)
- On click, opens a panel with an iframe → `/embed`
- Close button inside the panel posts `intelliforge-chat-close` to collapse it
- Mobile: panel expands to ~85vh from the bottom

Optional attributes:
- `data-position="bottom-left"` — move launcher to the left
- `data-base="https://masterclass-first-agent.vercel.app"` — override widget origin (defaults to script origin)

## Alternative — direct iframe (only if script tag won't work)

```html
<iframe
  src="https://masterclass-first-agent.vercel.app/embed"
  title="IntelliForge Bootcamp Assistant"
  style="position:fixed;bottom:24px;right:24px;width:min(400px,calc(100vw - 32px));height:min(620px,calc(100dvh - 120px));border:none;border-radius:14px;z-index:9999;box-shadow:0 20px 60px rgba(0,0,0,.45)"
  allow="clipboard-write"
></iframe>
```

Prefer the script tag approach — it includes the launcher button and open/close behavior.

## Implementation tasks

1. Find the global layout or HTML shell used by every page on upskill.intelliforge.tech.
2. Add the `embed.js` script tag so the widget appears on all marketing pages (home, pricing, FAQ, curriculum, contact).
3. Ensure nothing blocks it:
   - No CSP `frame-src` or `script-src` that blocks `masterclass-first-agent.vercel.app`
   - No `z-index` stacking context on the footer/fixed nav that hides the launcher (widget uses z-index ~2147483645)
4. Do NOT add a duplicate chat UI — the widget is self-contained.
5. Verify locally and in preview:
   - Launcher appears bottom-right
   - Clicking opens the chat panel
   - Asking "What does the 12-week bootcamp cost?" returns an answer
   - Close button collapses the panel

## Notes

- First API call after idle can take ~30s (Fly.io cold start). The widget shows a warming indicator during this.
- The assistant answers from the IntelliForge bootcamp FAQ (pricing, build-alongside, credential, curriculum, etc.).
- Widget styling is dark slate + green launcher — it should not clash with the upskill site, but avoid placing other fixed bottom-right CTAs in the same corner.

## Out of scope

- Do not modify the masterclass-first-agent repo
- Do not rebuild the chat backend or RAG pipeline
- Only integrate the existing embed snippet into this upskill site
````

---

## Implementation checklist

1. Find the global layout or HTML shell used by every page on upskill.intelliforge.tech.
2. Add the `embed.js` script tag so the widget appears on all marketing pages (home, pricing, FAQ, curriculum, contact).
3. Ensure nothing blocks it:
   - No CSP `frame-src` or `script-src` that blocks `masterclass-first-agent.vercel.app`
   - No `z-index` stacking context on the footer/fixed nav that hides the launcher (widget uses z-index ~2147483645)
4. Do **not** add a duplicate chat UI — the widget is self-contained.
5. Verify locally and in preview:
   - Launcher appears bottom-right
   - Clicking opens the chat panel
   - Asking "What does the 12-week bootcamp cost?" returns an answer
   - Close button collapses the panel

---

## Notes

- **Cold start:** The first API call after idle can take ~30s while Fly.io wakes the machine. The widget shows a warming indicator during this. To eliminate cold starts, set `min_machines_running = 1` in `fly.toml`.
- **Knowledge base:** Answers are grounded in `data/intelliforge-faq.md`, ingested into Chroma at deploy time. After updating the FAQ, run `uv run python -m scripts.ingest` and redeploy the Fly backend.
- **CORS:** The backend allows `https://upskill.intelliforge.tech` and `https://*.intelliforge.tech`. Add more origins via the `CORS_ALLOWED_ORIGINS` env var on Fly.
- **Framing:** `web/next.config.ts` sets `frame-ancestors` on `/embed` for upskill and localhost dev.

---

## Source files in this repo

| File | Purpose |
|------|---------|
| `web/public/embed.js` | Script-tag loader (launcher + iframe panel) |
| `web/src/app/embed/page.tsx` | Embed route |
| `web/src/components/EmbedPanel.tsx` | Compact chat panel shell |
| `web/src/components/ChatInterface.tsx` | Chat UI (`variant="embed"`) |
| `web/next.config.ts` | `frame-ancestors` CSP for iframe embedding |
| `src/server.py` | CORS config for cross-origin API calls |

---

## Redeploy after changes

```bash
# Re-ingest FAQ if data/intelliforge-faq.md changed
uv run python -m scripts.ingest

# Backend (includes updated .chroma at build time)
fly deploy

# Frontend (widget + embed.js)
cd web && vercel --prod
```
