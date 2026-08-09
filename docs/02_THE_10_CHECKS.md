# 02 — The 10 Checks Explained

This is the most important document in the project.

---

## 1. Lint

Tool:

```text
Ruff
```

Command:

```bash
ruff check app tests scripts
```

Question it answers:

> Does the Python code contain obvious style, quality, or programming mistakes?

Examples:

- unused imports,
- undefined names,
- some bad coding patterns.

Mental model:

```text
Lint = Grammar checker for code
```

---

## 2. Type Check

Tool:

```text
mypy
```

Command:

```bash
mypy app scripts
```

Question:

> Are we using values in ways that match our type hints?

Example:

```python
def add(a: int, b: int) -> int:
    return a + b
```

A type checker can catch code that tries to pass the wrong kind of value.

Mental model:

```text
Type check = Are the shapes of our data consistent?
```

---

## 3. Unit Tests

Tool:

```text
pytest
```

Command:

```bash
pytest -q
```

Question:

> Does the application behave the way we expect?

Examples in this project:

- health returns 200,
- redaction removes SSN,
- API key is required,
- tokenization is repeatable.

Mental model:

```text
Unit tests = Does the software work?
```

---

## 4. Coverage

Tool:

```text
pytest-cov
```

Command:

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

Question:

> How much of our application code did the tests actually execute?

Coverage is not proof that the software is correct.

It is a visibility measure.

Mental model:

```text
Tests = Did checks pass?

Coverage = How much code did those checks touch?
```

---

## 5. SAST

Tool:

```text
Bandit
```

SAST means:

```text
Static Application Security Testing
```

Command:

```bash
bandit -r app -q
```

Question:

> Can we find security problems by examining source code without running the application?

Examples might include:

- unsafe functions,
- weak security patterns,
- risky Python usage.

Mental model:

```text
SAST = Security review of the code itself
```

---

## 6. Dependency Scan

Tool:

```text
pip-audit
```

Command:

```bash
pip-audit -r requirements.txt
```

Question:

> Do any third-party Python packages we use have known vulnerabilities?

Our code may be secure while a library has a published vulnerability.

Mental model:

```text
Dependency scan = Are the ingredients we imported safe?
```

---

## 7. Secret Scan

Tool:

```text
Trivy
```

Question:

> Did someone accidentally commit a credential or secret to the repository?

Examples:

- API keys,
- tokens,
- private keys,
- passwords.

Mental model:

```text
Secret scan = Did we accidentally put a key in the code box?
```

Why it matters:

Removing a secret from the latest file may not be enough because Git keeps history.

A real exposed credential should usually be revoked or rotated.

---

## 8. Privacy Policy Check

Tool:

```text
scripts/privacy_check.py
```

This is our own small check.

Question:

> Does our application violate a few privacy/security rules that we care about?

It looks for simple examples such as:

- hard-coded passwords,
- hard-coded API keys,
- printing request objects.

This demonstrates:

```text
Policy as Code
```

Instead of only saying:

> Do not hard-code secrets.

we write a machine-readable rule that can fail the pipeline.

Mental model:

```text
Privacy policy check = Turn one policy into executable code
```

---

## 9. IaC Scan

Tool:

```text
Trivy
```

IaC means:

```text
Infrastructure as Code
```

Our infrastructure files are:

```text
k8s/deployment.yaml
k8s/service.yaml
```

Question:

> Are there obvious insecure infrastructure configurations?

Examples in real systems:

- containers running as root,
- excessive privileges,
- dangerous network exposure,
- insecure cloud resources.

Mental model:

```text
IaC scan = Security review of deployment instructions
```

---

## 10. DAST

Tool:

```text
OWASP ZAP
```

DAST means:

```text
Dynamic Application Security Testing
```

Unlike SAST, the application must be running.

Workflow:

```text
Start FastAPI
     ↓
ZAP sends HTTP requests
     ↓
Observe application responses
```

Question:

> Can we find security problems by interacting with the running application from the outside?

Mental model:

```text
SAST = Read the code

DAST = Test the running application
```

---

# Why the order makes sense

```text
Cheap / fast checks first
        ↓
More expensive checks later
```

We do not want to start a DAST scanner if basic unit tests already fail.

That is why the pipeline starts with linting and ends with running-application testing.

---

# One-line memory trick

```text
Lint = code quality
Type = data correctness
Tests = behavior
Coverage = test reach
SAST = source security
Dependency = package security
Secret = credential leakage
Privacy = our custom rules
IaC = infrastructure security
DAST = running application security
```
