# FastSME

The landing site for **FastSME** — an open-source platform bringing enterprise-grade software to SMEs and SMBs globally at affordable prices.

FastSME is operated by Exroad Fintech Ltd and the source is published at [github.com/predictivelabsai](https://github.com/predictivelabsai).

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The app listens on `http://localhost:5001` by default and honours the `PORT` environment variable.

## Tests

```bash
pip install pytest playwright
python -m playwright install chromium
python -m pytest tests/test_pages.py -v
```

Browser artifacts are written to `output/playwright/`.

## Docker

```bash
docker build -t fastsme .
docker run --rm -p 5001:5001 fastsme
curl http://localhost:5001/healthz
```

See [DEPLOY.md](DEPLOY.md) for the Coolify and CI/CD setup.

## Structure

- `app.py` — routes, redirects and page composition
- `components.py` — shared layout and design system
- `content/products.py` — grouped Fast* product portfolio
- `content/clients.py` — selected client experience
- `content/team.py` — core team and advisory board
- `static/` — CSS and favicon

## Legal

Exroad Fintech Ltd, trading as FastSME<br>
Company number 11914994<br>
155 Minories Street, Flat 275, London, United Kingdom, EC3N 1AD<br>
Contact: info@fastsme.com
