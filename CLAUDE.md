# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Predictive Labs corporate landing site — a multi-page, server-rendered FastHTML app with a dark EU-blue palette, Tailwind CSS via CDN, Plotly data visualisations (Signal page), a Three.js globe hero, and a background RSS news feed with LLM-based relevance filtering.

## Commands

```bash
# Run dev server (serves on http://localhost:5001)
python main.py

# Run tests (requires playwright + chromium)
pip install playwright pytest && python -m playwright install chromium
python -m pytest tests/test_pages.py -v

# Install dependencies
pip install -r requirements.txt

# Docker
docker build -t plai-landing . && docker run -p 5001:5001 plai-landing
```

## Architecture

**Entrypoint chain:** `main.py` (thin shim for Docker CMD) → `app.py` (all routes + `fast_app()`) → `components.py` (shared layout, design tokens, reusable components).

**Rendering model:** Pure server-side HTML. Every page is composed via `page()` in `components.py`, which assembles `<html>` with Navbar, Main, Footer, Tailwind CDN config, and optional per-page scripts. No client-side framework; interactivity is vanilla JS (Plotly charts, Three.js globe, mobile nav toggle).

**Content layer** (`content/`):
- `case_studies.py` — structured dicts (`BID_DERIVED`, `NAMED_PRECEDENTS`, `ALL`)
- `team.py` — `TEAM` list
- `repos.py` — `REPOS` + `EXTERNAL_RESEARCH`
- `signal.py` — reads CSVs from `content/data/`, builds Plotly trace dicts server-side, served as JSON to the client
- `news.py` — background daemon thread fetches RSS/Atom feeds hourly, caches in-memory per category, filters via keyword regex + OpenRouter LLM classifier (fail-open if no API key)

**Routes** (all in `app.py`):
`/`, `/platform`, `/solutions/{defense,healthcare,public,financial}`, `/case-studies`, `/signal`, `/research`, `/team`, `/contact`

**Static assets** (`static/`):
- `site.css` — custom styles (signal tabs, chart frames, scroll reveal, scrollbar)
- `signal.js` — Plotly rendering + tab switching
- `three-hero.js` — Three.js globe (ES module)
- `video/` — compressed hero background video

## Key Patterns

- **Tailwind config is inline JS** in `components.py` (`TAILWIND_CONFIG`). Color tokens: `bg`, `ink`, `line`, `accent` — each with sub-shades. All custom colors live there, not in CSS.
- **`Section_()` wrapper** adds max-width container + responsive padding. Most page sections use it.
- **`SectorLink()`** creates cross-links between sector pages using the `SECTOR_HREF` lookup map in `components.py`.
- **Solution pages** are data-driven via the `SOLUTIONS` dict in `app.py` — `_solution_page(slug)` renders all four.
- **News filtering** has two layers: `_DROP_RE` regex for obvious admin noise, then `_llm_classify()` via OpenRouter (needs `OPENROUTER_API_KEY` env var; optional `httpx` dependency).
- **Signal data** is static CSVs with `.SOURCE.md` provenance files alongside each.

## Environment Variables

- `OPENROUTER_API_KEY` — enables LLM-based news filtering (optional; falls back to keyword-only)
- `NEWS_FILTER_MODEL` — override the OpenRouter model (default: `anthropic/claude-haiku-4-5`)
- `PORT` — server port (default: 5001)

## Tests

`tests/test_pages.py` uses Playwright to boot the app on port 5011, visit every route, assert the `<h1>` contains expected text, and save full-page screenshots to `screenshots/`. Tests are parametrised by route.
