# Beginner Privacy DevSecOps — Continuous Workflow

This repository keeps the application small, but keeps the **full learning workflow**:

```text
Lint
  ↓
Type Check
  ↓
Unit Tests
  ↓
Coverage
  ↓
SAST
  ↓
Dependency Scan
  ↓
Secret Scan
  ↓
Privacy Policy Check
  ↓
IaC Scan
  ↓
Start FastAPI
  ↓
DAST
  ↓
Docker Build
```

The important design choice is that everything runs in **one GitHub Actions job, from top to bottom**.

That makes the workflow easy to read and explain.

---

# What the project does

The FastAPI application exposes:

| Endpoint | Purpose |
|---|---|
| `GET /health` | Shows that the app is alive |
| `POST /redact` | Redacts simple email and SSN patterns |
| `POST /tokenize` | Creates a simple pseudonymous identifier |

The project is intentionally small so the **workflow**, not the application complexity, is the main learning experience.

---

# The complete architecture

```text
Developer
    |
    | git push / pull request
    v
GitHub
    |
    v
GitHub Actions
    |
    v
+--------------------------------+
| 1. Lint                        |
| 2. Type Check                  |
| 3. Unit Tests                  |
| 4. Coverage                    |
| 5. SAST                        |
| 6. Dependency Scan             |
| 7. Secret Scan                 |
| 8. Privacy Policy Check        |
| 9. IaC Scan                    |
| 10. DAST                       |
+--------------------------------+
    |
    v
Docker Build
    |
    v
Docker Image
    |
    v
Kubernetes Example
    |
    v
FastAPI Pods
```

---

# Why this is still beginner-friendly

The first version of a DevSecOps pipeline can become confusing because people often create:

- many jobs,
- many branches,
- separate workflows,
- matrix builds,
- production deployments,
- artifact signing,
- registries,
- environment approvals.

This repository deliberately avoids those.

There is:

```text
ONE workflow file
ONE job
ONE straight sequence
```

Every step has a number.

If Step 3 fails, Step 4 normally does not run.

That is the basic concept of a pipeline.

---

# Project structure

```text
beginner-privacy-devsecops-continuous/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   └── test_main.py
│
├── scripts/
│   └── privacy_check.py
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   ├── 01_PROJECT_FROM_ZERO.md
│   ├── 02_THE_10_CHECKS.md
│   ├── 03_CICD_WORKFLOW.md
│   ├── 04_FILE_BY_FILE.md
│   ├── 05_INTERVIEW_GUIDE.md
│   └── 06_WHAT_TO_ADD_LATER.md
│
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# Run locally

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install everything:

```bash
pip install -r requirements-dev.txt
```

Run FastAPI:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Run the beginner checks locally

```bash
ruff check app tests scripts

mypy app scripts

pytest -q

pytest --cov=app --cov-report=term-missing

bandit -r app -q

pip-audit -r requirements.txt

python scripts/privacy_check.py
```

The Trivy and ZAP examples are mainly demonstrated in GitHub Actions because they are easiest to understand there.

---

# What to learn first

Use this order:

```text
1. app/main.py
2. tests/test_main.py
3. scripts/privacy_check.py
4. Dockerfile
5. .github/workflows/ci.yml
6. k8s/deployment.yaml
7. k8s/service.yaml
```

Then read:

```text
docs/02_THE_10_CHECKS.md
```

That document explains exactly what each check means.

---

# 60-second interview explanation

> I built a deliberately small FastAPI privacy demo so I could focus on the software delivery pipeline. A GitHub push triggers one continuous CI workflow. It starts with code-quality controls—linting and type checking—then runs unit tests and coverage. Next it performs security checks using Bandit for SAST, pip-audit for dependency vulnerabilities, Trivy for secret scanning, a custom privacy policy check, and Trivy again for Kubernetes Infrastructure-as-Code scanning. The pipeline then starts the FastAPI application and uses OWASP ZAP for a basic DAST scan against the running service. Finally, it builds the Docker image. I also included a small Kubernetes Deployment and Service to show where that image would run. The goal is to demonstrate how privacy and security controls can become part of a continuous engineering workflow rather than a manual review at the end.

---

# Important

This is a **learning repository**, not a production healthcare application.

Some checks are configured to teach the process rather than enforce enterprise-grade thresholds.

The documentation explains where production hardening would be added later.
