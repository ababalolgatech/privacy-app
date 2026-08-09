# 06 — What to Add Later

Do not add these until you understand the existing project.

## Next Level 1 — Docker image scan

After:

```text
docker build
```

scan the built container image for vulnerabilities.

## Next Level 2 — Container registry

Push the approved image to:

- GitHub Container Registry,
- Azure Container Registry,
- AWS ECR,
- another approved registry.

## Next Level 3 — Real Kubernetes secrets

Do not put demo secrets directly in YAML.

Use:

- Kubernetes Secret,
- external secrets operator,
- Azure Key Vault,
- AWS Secrets Manager,
- HashiCorp Vault,
- similar enterprise service.

## Next Level 4 — Strong identity

Replace the demo API key with:

- OAuth 2.0,
- OpenID Connect,
- workload identity,
- mTLS where appropriate.

## Next Level 5 — CD

Add:

```text
Build
 ↓
Registry
 ↓
Staging
 ↓
Approval
 ↓
Production
```

## Next Level 6 — Parallelize

Once you understand the straight pipeline, independent checks can run in parallel to reduce CI time.

Learning order:

```text
First understand sequential flow.
Then optimize.
```
