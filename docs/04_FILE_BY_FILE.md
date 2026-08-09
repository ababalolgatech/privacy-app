# 04 — File-by-File Guide

## `app/main.py`

The actual FastAPI application.

Learn:

- endpoints,
- request models,
- environment variables,
- basic authentication,
- redaction,
- pseudonymization.

## `tests/test_main.py`

Automated tests.

Learn:

- TestClient,
- status codes,
- assertions,
- privacy-focused assertions.

## `scripts/privacy_check.py`

Custom beginner policy-as-code.

Learn:

- scan source files,
- detect simple patterns,
- return exit code 1 when a policy fails.

CI uses exit codes to decide whether a step passed.

## `requirements.txt`

Production/runtime dependencies.

## `requirements-dev.txt`

Developer and CI tools.

It includes:

- pytest,
- coverage,
- Ruff,
- mypy,
- Bandit,
- pip-audit.

Keeping runtime and development tools separate is a common practice.

## `Dockerfile`

Packages the application into a container image.

## `.github/workflows/ci.yml`

The heart of this learning project.

Read it from top to bottom.

It shows the continuous flow.

## `k8s/deployment.yaml`

Tells Kubernetes:

- which image to run,
- how many replicas,
- which port,
- which environment variables,
- how to check health.

## `k8s/service.yaml`

Provides a stable Kubernetes service endpoint for the matching Pods.
