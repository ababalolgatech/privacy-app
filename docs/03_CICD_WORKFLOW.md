# 03 — The Continuous CI/CD Workflow

The entire workflow is in:

```text
.github/workflows/ci.yml
```

There is only:

```text
ONE JOB
```

called:

```text
continuous-checks
```

## The flow

```text
Git Push / Pull Request
          ↓
Checkout
          ↓
Set up Python
          ↓
Install packages
          ↓
1. Lint
          ↓
2. Type Check
          ↓
3. Unit Tests
          ↓
4. Coverage
          ↓
5. SAST
          ↓
6. Dependency Scan
          ↓
7. Secret Scan
          ↓
8. Privacy Policy Check
          ↓
9. IaC Scan
          ↓
Start FastAPI
          ↓
10. DAST
          ↓
11. Docker Build
```

## Why this is beginner-friendly

Many enterprise pipelines use parallel jobs.

For example:

```text
        ┌→ SAST
Build ──┼→ Unit Tests
        └→ SCA
```

Parallel workflows are faster, but harder to understand at first.

This repository deliberately uses:

```text
A → B → C → D
```

so you can read it like a story.

## What happens when a check fails?

Normally:

```text
Step fails
   ↓
Job fails
   ↓
Later steps stop
```

This is called a:

```text
quality gate
```

or:

```text
security gate
```

depending on the check.

## Why IaC is currently informational

The sample Kubernetes YAML is intentionally simple.

The Trivy IaC step uses:

```text
exit-code: 0
```

so findings are shown without blocking the beginner pipeline.

In a more mature environment, you would change it to:

```text
exit-code: 1
```

after fixing the Kubernetes security findings and agreeing on policy.

That illustrates an important real-world DevSecOps concept:

> Introduce visibility first, tune the rules, then enforce the gate.

## Why ZAP does not fail the workflow

The beginner DAST action uses:

```text
fail_action: false
```

because baseline ZAP scans can report informational findings that need tuning.

In production, the team would:

1. review findings,
2. reduce false positives,
3. define accepted thresholds,
4. turn selected findings into blocking controls.

This is more realistic than pretending every scanner should block immediately.

## Where CD would begin

After Docker build:

```text
Docker Image
      ↓
Push to Registry
      ↓
Deploy to Kubernetes
```

Those are deliberately not automated here.

The project teaches the boundary between:

```text
CI = validate/build

CD = deliver/deploy
```
