# Privacy DevSecOps FastAPI Demo

A small interview-ready GitHub project that connects:

**FastAPI + Python + Ubuntu + Docker + Kubernetes + CI/CD + DevSecOps + Privacy Engineering**

It is intentionally small enough to explain in an interview while demonstrating a broad set of technical skills expected of a Lead Data Privacy Engineer working with software and platform teams.

> **Educational demo:** The tokenization logic uses HMAC pseudonymization to demonstrate the concept. It is **not** a production token vault or healthcare security architecture.

---

## 1. What the application does

The FastAPI service exposes four endpoints:

| Endpoint | Purpose | Auth |
|---|---|---|
| `GET /health/live` | Kubernetes/container liveness | No |
| `GET /health/ready` | Kubernetes readiness | No |
| `POST /v1/tokenize` | Convert a sensitive value into a deterministic HMAC token | `X-API-Key` |
| `POST /v1/redact` | Redact email, SSN, and payment-card-like strings | `X-API-Key` |

Example:

```bash
curl -X POST http://localhost:8000/v1/tokenize \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: local-demo-api-key-change-me' \
  -d '{"value":"123-45-6789","purpose":"member correlation"}'
```

The response returns a token and does not echo the raw value.

---

## 2. Architecture

```text
Developer
   |
   v
GitHub / Pull Request
   |
   v
CI Pipeline
   |-- Ruff lint/format
   |-- mypy type checking
   |-- pytest + coverage gate
   |-- Bandit SAST
   |-- pip-audit dependency scan
   |-- CodeQL
   |-- Trivy repo/secret scan
   |-- Custom privacy-policy check
   |-- Trivy Kubernetes/IaC scan
   v
Docker Build
   |
   v
Trivy Container Scan
   |
   v
Container Registry
   |
   v
Kubernetes
   |-- Deployment / replicas
   |-- Liveness / readiness
   |-- Runtime securityContext
   |-- Secret reference
   |-- NetworkPolicy
   v
FastAPI
```

---

## 3. Skills demonstrated

### Software Engineering

- Python
- Typed models
- FastAPI
- API authentication
- Dependency injection
- Configuration management
- Unit testing
- Error handling
- Modular application structure

### Privacy Engineering

- Data minimization
- Pseudonymization/tokenization concept
- PII redaction
- Safe application logging
- Data classification concept
- Privacy policy automation
- Threat modeling
- Purpose-awareness

### DevOps / DevSecOps

- GitHub Actions
- CI quality gates
- Docker image build
- Ubuntu container foundation
- Container vulnerability scanning
- SAST
- SCA/dependency scanning
- Secret scanning
- Infrastructure-as-Code scanning
- Dependabot

### Kubernetes

- Deployment and replicas
- Service
- Liveness/readiness probes
- Resource limits
- Non-root workload
- Read-only root filesystem
- Capability dropping
- No privilege escalation
- NetworkPolicy
- Runtime secret injection

---

## 4. Run locally

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install:

```bash
pip install -r requirements-dev.txt
```

Run:

```bash
uvicorn app.main:app --reload
```

Open API documentation:

```text
http://localhost:8000/docs
```

---

## 5. Run the checks locally

```bash
make check
```

Or separately:

```bash
ruff check app tests scripts
ruff format --check app tests scripts
mypy app
pytest --cov=app --cov-report=term-missing --cov-fail-under=85
bandit -q -r app
pip-audit -r requirements.txt
python scripts/privacy_check.py .
```

The GitHub Actions workflow additionally runs Trivy against the repository, Kubernetes configuration, and built container image.

---

## 6. Docker

Build:

```bash
docker build -t privacy-devsecops-demo:local .
```

Run with local-only demo values:

```bash
docker run --rm -p 8000:8000 \
  -e APP_ENV=local \
  -e DEMO_API_KEY=local-demo-api-key-change-me \
  -e TOKENIZATION_KEY=local-demo-token-key-change-me \
  privacy-devsecops-demo:local
```

### Docker security choices

- Ubuntu 24.04 foundation
- Minimal installed OS packages
- Python virtual environment
- Non-root user (`10001`)
- No secrets copied into the image
- Health check
- `.dockerignore`

---

## 7. Kubernetes

The `k8s/` folder demonstrates:

```text
Deployment -> Pods -> Container -> Ubuntu -> Python -> FastAPI
```

The Deployment asks Kubernetes to keep two replicas running.

Before a real deployment:

1. Replace the image placeholder.
2. Create `privacy-demo-secrets` through a secure secret-management workflow.
3. Validate ingress/egress policy for the target cluster.
4. Pin production image by immutable digest rather than `latest`.

Example secret creation for a disposable local lab only:

```bash
kubectl create secret generic privacy-demo-secrets \
  --from-literal=api-key='replace-me' \
  --from-literal=tokenization-key='replace-me-too'
```

Do not commit exported secret YAML containing real values.

---

## 8. CI/CD checks and why they matter

| Check | Tool / File | What it demonstrates |
|---|---|---|
| Lint/format | Ruff | Engineering quality |
| Type checking | mypy | Safer interfaces/contracts |
| Unit tests | pytest | Correctness |
| Coverage gate | pytest-cov | Test discipline |
| SAST | Bandit + CodeQL | Source-code security |
| DAST | OWASP ZAP baseline | Test the running API from the outside |
| Dependency audit | pip-audit | Software composition risk |
| Secret scan | Trivy | Prevent credentials in source |
| Privacy rule | `privacy_check.py` | Privacy policy as automated control |
| IaC scan | Trivy config | Kubernetes misconfiguration detection |
| Container scan | Trivy image | OS/package vulnerability detection |
| Dependency updates | Dependabot | Supply-chain hygiene |
| Continuous Delivery | GHCR + staging artifact | Immutable image publication and environment-gated promotion |

---

## 9. Privacy engineering discussion points

### Why not log the raw value?

A centralized log platform is another data store. Logging PII/PHI increases data copies, access scope, breach impact, and retention complexity.

### Is HMAC really tokenization?

It is a useful **pseudonymization demonstration**, not a full enterprise tokenization vault. A production design may require a reversible token service, KMS/HSM integration, key rotation, audited detokenization, separation of duties, and defined cryptographic standards.

### Why an API key if OAuth is better?

The API key keeps the demo small. In an enterprise architecture, discuss OAuth/OIDC, mTLS, workload identity, managed identities, short-lived credentials, and least privilege.

### Why reference Kubernetes Secrets if they have limitations?

The manifest demonstrates that secrets are supplied at runtime rather than committed. A production design should consider an external secrets manager, encryption at rest, workload identity, access auditing, and key rotation.

---

## 10. What to say in an interview

A concise explanation:

> I built a small FastAPI service to demonstrate how privacy engineering can be embedded into the software lifecycle. The application uses authentication, Pydantic validation, pseudonymization, and redacted logging. The CI pipeline checks code quality, types, tests, security vulnerabilities, dependencies, secrets, privacy rules, Kubernetes configuration, and the final container image. Docker provides a repeatable Ubuntu-based runtime, and Kubernetes demonstrates deployment, health checks, least-privilege workload settings, secrets, and networking. The purpose is to show how a privacy requirement can become an automated technical guardrail rather than remain only in a policy document.

See [`docs/interview-map.md`](docs/interview-map.md) for a question-to-file mapping.

---

## 11. Production improvements to discuss

A good interview answer should acknowledge what you would strengthen in production:

- OAuth/OIDC or workload identity instead of a static API key
- Enterprise token vault/KMS/HSM
- Reversible tokenization only where justified
- Key rotation strategy
- API gateway/WAF
- TLS/mTLS
- Central secret manager
- Distributed tracing with sensitive-field controls
- SIEM integration
- Audit-event schema
- Data retention/deletion automation
- DLP/DSPM integrations
- Signed images and provenance attestations
- Pin GitHub Actions to immutable commit SHAs
- Immutable container image digests in Kubernetes
- Admission control / policy-as-code (OPA Gatekeeper, Kyverno, or equivalent)
- GitOps deployment / environment approvals
- Cloud IAM and network segmentation
- Automated PIA/privacy review triggers for high-risk changes

---

## 12. Repository structure

```text
privacy-devsecops-fastapi-demo/
├── app/
│   ├── config.py
│   ├── logging_utils.py
│   ├── main.py
│   ├── models.py
│   └── privacy.py
├── tests/
├── scripts/
│   └── privacy_check.py
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── network-policy.yaml
├── docs/
│   ├── architecture.md
│   ├── interview-map.md
│   └── threat-model.md
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── codeql.yml
│   │   ├── dast.yml
│   │   └── cd.yml
│   ├── dependabot.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── Dockerfile
├── Makefile
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```
