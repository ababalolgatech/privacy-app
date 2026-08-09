# 01 — Project From Zero

This guide assumes you are new to software engineering.

## The central idea

We have one tiny application.

```text
FastAPI
```

We want confidence that it is:

```text
Readable
Correct
Tested
Reasonably secure
Privacy-aware
Packageable
Deployable
```

Instead of checking these things manually, we create a pipeline.

```text
Code
 ↓
Automated Checks
 ↓
Docker Image
 ↓
Deployment Platform
```

## The application

`app/main.py` is the actual software.

FastAPI gives us URLs called endpoints.

```text
GET /health
POST /redact
POST /tokenize
```

`/health` helps operations know whether the app is alive.

`/redact` demonstrates removing sensitive-looking values.

`/tokenize` demonstrates replacing an identifier with a pseudonymous value.

## What GitHub Actions does

GitHub Actions creates a temporary Ubuntu computer.

It:

1. downloads our repository,
2. installs Python,
3. installs our packages,
4. runs every check in order.

This temporary computer is called a **runner**.

## Why continuous?

The pipeline is continuous because one check flows into the next.

```text
Lint → Type → Test → Security → Privacy → Infrastructure → DAST → Build
```

If an important early step fails, the workflow normally stops.

That prevents a bad change from moving farther through the software delivery process.

## CI vs CD

This repository mainly demonstrates **CI**.

CI:

```text
Does the code pass our checks?
```

CD would continue:

```text
Push image to registry
 ↓
Deploy to staging
 ↓
Approval
 ↓
Deploy to production
```

We intentionally leave those production steps out so the beginner workflow stays understandable.
