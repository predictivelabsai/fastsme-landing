# FastSME landing site

FastSME is an open-source platform bringing enterprise-grade software to SMEs and SMBs globally at affordable prices. The site is a multi-page, server-rendered FastHTML application with a light green visual system.

## Commands

```bash
python main.py
python -m pytest tests/test_pages.py -v
docker build -t fastsme .
docker run --rm -p 5001:5001 fastsme
```

## Architecture

- `main.py` starts uvicorn and honours `$PORT`.
- `app.py` defines pages, legacy redirects, canonical-host middleware and operational endpoints.
- `components.py` contains the shared navigation, footer, SEO head, design tokens and UI primitives.
- `content/products.py` is the source of truth for the grouped Fast* portfolio.
- `content/clients.py` contains selected client experience.
- `content/team.py` contains the operating team and advisory board.
- `static/site.css` holds the small amount of CSS not expressed through Tailwind.

Primary routes are `/`, `/products`, `/clients`, `/open-source`, `/thesis`, `/team` and `/contact`.

## Brand and content rules

- Canonical brand: **FastSME**
- Canonical domain: `https://fastsme.com`
- Contact: `info@fastsme.com`
- Legal entity: Exroad Fintech Ltd, trading as FastSME, company number 11914994
- Position around SMEs/SMBs globally, open source, accessible economics and enterprise-grade capability.
- Keep positioning exclusively focused on SMEs, SMBs and their technology partners.
- Keep the 29-product portfolio data-driven, grouped around business jobs and filterable without hiding its server-rendered content from crawlers.

## Deployment

The Dockerfile is the deployment source of truth. Coolify targets port 5001 and checks `/healthz`. See `DEPLOY.md`. GitHub Actions tests every pull request and push to `main`; an optional secret webhook triggers Coolify after successful tests.
