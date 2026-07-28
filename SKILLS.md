# FastSME site capabilities

## Product portfolio

`content/products.py` contains 23 open-source Fast* products grouped into six practical categories. The same data powers the homepage featured cards and full `/products` catalog.

## Client experience

`content/clients.py` contains selected named engagements across technology, finance, industry, healthcare, retail, energy and real estate. Keep descriptions concise and exclude confidential details.

## Team

`content/team.py` contains the seven-person core team and four-person advisory board. Both are rendered on `/team`.

## SEO and operations

- Canonical metadata targets `fastsme.com`.
- `fastsme.org`, `www.fastsme.org` and `www.fastsme.com` redirect to the canonical host.
- `/robots.txt` and `/sitemap.xml` are generated in the application.
- `/healthz` supports Docker and Coolify health checks.

## Validation

`tests/test_pages.py` runs browser smoke tests for every primary route, checks removal of the old brand, exercises the mobile menu, verifies health, and checks a legacy redirect. Artifacts are written to `output/playwright/`.

## Deployment

See `DEPLOY.md` for Coolify domains, port, health checks, DNS and the two supported CI/CD modes.
