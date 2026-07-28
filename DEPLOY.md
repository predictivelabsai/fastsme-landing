# Deploying FastSME on Coolify

FastSME is a stateless FastHTML/uvicorn service deployed from the public GitHub repository `predictivelabsai/fastsme-landing`.

## Coolify resource

1. Create a resource from the public GitHub repository and select branch `main`.
2. Select **Dockerfile** as the build pack.
3. Set the exposed port to `5001`.
4. Set the health-check path to `/healthz`.
5. Add `https://fastsme.com` and `https://www.fastsme.com` as domains.
6. Later add `https://fastsme.org` and `https://www.fastsme.org` to the same resource. The application redirects those hosts to `https://fastsme.com`.
7. Enable automatic deployment from the repository.

No database, persistent volume or application secrets are required.

## DNS and TLS

Point the apex and `www` records for each domain to the Coolify host. Coolify will provision TLS certificates after the domains resolve. `fastsme.com` is the canonical origin.

## CI/CD

The GitHub Actions workflow runs import checks and browser smoke tests on pull requests and pushes to `main`. Deployment can work in either of two modes:

- Recommended: connect Coolify's GitHub App and enable auto-deploy after pushes to `main`.
- Webhook: add a repository secret named `COOLIFY_DEPLOY_WEBHOOK`; the workflow calls it only after tests pass on `main`.

The webhook URL is sensitive and must stay in GitHub Actions secrets.

## Verification

```bash
curl -fsS https://fastsme.com/healthz
curl -I https://fastsme.org/
```

The first command should return `{"status":"ok","service":"fastsme"}`. Once the `.org` domain is attached, the second should return a permanent redirect to `https://fastsme.com/`.
