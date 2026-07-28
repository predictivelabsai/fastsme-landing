# Skills

Capabilities of the **Predictive Labs corporate landing site** — a multi-page,
server-rendered FastHTML app (dark EU-blue palette, Tailwind via CDN) that
presents the company, its sector solutions, open-source portfolio and public
thesis. Live at **https://www.predictivelabs.ai**.

## Site & Pages

Pure server-side HTML composed via `page()` in `components.py` (Navbar + Main +
Footer + Tailwind config + per-page scripts). No client framework; interactivity
is vanilla JS.

| Route | Page |
|---|---|
| `/` | Home — hero, positioning, public-good framing |
| `/platform` | Platform overview |
| `/solutions/{defense,healthcare,public,financial}` | Four data-driven sector pages (`SOLUTIONS` dict in `app.py`) |
| `/case-studies` | Engagements & named precedents (`content/case_studies.py`) |
| `/signal` | Public-sector data visualisations (Plotly) |
| `/open-source` | Open-source ethos + toolkit cards (`content/repos.py`); `/research` 301-redirects here |
| `/thesis` | Digital-sovereignty thesis; links the EC Open Source Strategy |
| `/team` | Team bios (`content/team.py`) |
| `/contact` | Contact / programme enquiry |

## Internationalisation

`utils/i18n.py` — every user-facing string keyed in **12 languages**
(en, et, de, fr, sv, lv, no, da, pl, nl, fi, lt). Views call `t(key, lang)`;
language is resolved per request and switchable in the navbar.

## Signal — data visualisations

`content/signal.py` reads CSVs from `content/data/` (each with a `.SOURCE.md`
provenance file), builds Plotly trace dicts server-side, and serves them as JSON
to `static/signal.js` which renders the charts + tab switching.

## Three.js globe hero

`static/three-hero.js` (ES module) renders an interactive globe on the hero,
over a compressed background video in `static/video/`.

## Background news feed

`content/news.py` runs a daemon thread that fetches RSS/Atom feeds hourly,
caches them per category in-memory, and filters via a keyword regex (`_DROP_RE`)
plus an optional OpenRouter LLM classifier (`_llm_classify`, fail-open without a
key).

## Open-source portfolio cards

The `/open-source` page renders one card per entry in `content/repos.py`
(`REPOS`) — name, tagline, tags, relevance — linking each
`github.com/predictivelabsai/*` demonstrator, plus external research platforms
(`EXTERNAL_RESEARCH`). Add a repo by appending a dict; the card appears on next
deploy.

## Architecture

`main.py` (Docker shim) → `app.py` (all routes + `fast_app()`) →
`components.py` (shared layout, design tokens, reusable components). Tailwind
colour tokens (`bg`, `ink`, `line`, `accent`) live inline in `TAILWIND_CONFIG`
in `components.py`. See `CLAUDE.md` for the full architecture.

## Commands

```bash
python main.py                                   # dev server → http://localhost:5001
pip install -r requirements.txt                  # dependencies
python -m pytest tests/test_pages.py -v           # Playwright route smoke tests → screenshots/
docker build -t plai-landing . && docker run -p 5001:5001 plai-landing
```

## Deployment & CI/CD

Deployed on **Coolify** (`coolify.finespresso.org`, finespresso-server) as the
`predictivelabsai/predictivelabsai-landing` application, serving
`www.predictivelabs.ai` / `predictivelabs.ai` / `predictivelabs.co.uk`.

- **Source:** Public GitHub, branch `main`.
- **CI/CD:** a GitHub **push webhook** on the repo posts to Coolify's manual
  webhook endpoint; with **Auto Deploy** enabled, every push to `main`
  rebuilds and rolling-redeploys the site. (Manual deploys: the Coolify
  "Redeploy" button, or the authenticated Deploy Webhook API.)

## Environment Variables

- `OPENROUTER_API_KEY` — enables LLM news filtering (optional; falls back to keyword-only)
- `NEWS_FILTER_MODEL` — OpenRouter model override (default `anthropic/claude-haiku-4-5`)
- `PORT` — server port (default 5001)
