# Interview Skill Map

Use this file to explain the repository during an interview.

| Interview topic | Where demonstrated | Talking point |
|---|---|---|
| Python | `app/` | Typed Python, modules, configuration, HMAC, regex |
| FastAPI / APIs | `app/main.py` | Routes, validation, dependency injection, authentication, lifecycle |
| Privacy by Design | `app/privacy.py`, tests | Data minimization, pseudonymization, redaction |
| Secure logging | `app/logging_utils.py` | Prevent PII/PHI leakage into logs |
| Unit testing | `tests/` | Positive/negative tests, privacy assertions |
| CI | `.github/workflows/ci.yml` | Automated quality/security/privacy checks |
| CD concept | README / workflow design | Build artifact ready for promotion; production deployment can require approval |
| Docker | `Dockerfile` | Ubuntu base, Python runtime, non-root container, health check |
| Container security | `Dockerfile`, CI | Minimal packages, no secrets, image vulnerability scanning |
| Kubernetes | `k8s/` | Deployments, replicas, probes, service, NetworkPolicy |
| DevSecOps | CI + K8s | Controls embedded into delivery rather than manual end-stage review |
| DAST | `.github/workflows/dast.yml` | Start the API and run an OWASP ZAP baseline scan |
| Continuous Delivery | `.github/workflows/cd.yml` | Publish immutable image and prepare environment-gated deployment bundle |
| SAST | Bandit + CodeQL | Source code security analysis |
| SCA | `pip-audit` / Dependabot | Third-party dependency risk |
| Secret scanning | Trivy fs scan | Detect credentials before production |
| IaC security | Trivy config scan | Scan Kubernetes configuration |
| Policy as Code | `scripts/privacy_check.py` | Convert a privacy rule into an automated gate |
| IAM concepts | API key + K8s service token disabled | Authentication, least privilege, workload identity discussion |
| Secrets management | K8s `secretKeyRef` | Values injected at runtime; real secret not committed |
| Encryption/tokenization | `privacy.py` | HMAC pseudonymization; discuss KMS/HSM and token vaults |
| Threat modeling | `docs/threat-model.md` | Asset, threat, impact, control mapping |
| Observability | Health endpoints + safe logs | Liveness/readiness without exposing sensitive data |
| Software supply chain | CI + image scan + Dependabot | Validate code, dependencies, and container artifacts |

## 90-second project explanation

> This is a small privacy-focused FastAPI service designed to show how I would connect
> software engineering with DevSecOps and privacy engineering. The API demonstrates
> authentication, input validation, deterministic pseudonymization, and PII redaction.
> I package it in a non-root Ubuntu-based Docker image. The GitHub Actions pipeline
> runs linting, type checking, tests, coverage, SAST, dependency auditing, secret
> scanning, a custom privacy policy check, Kubernetes IaC scanning, and a container
> vulnerability scan. The Kubernetes manifests demonstrate desired state, health
> probes, resource limits, restricted runtime privileges, NetworkPolicy, and runtime
> secret injection. The point is not that every organization uses exactly these tools;
> it is that privacy requirements can be translated into automated engineering
> guardrails across the software lifecycle.
