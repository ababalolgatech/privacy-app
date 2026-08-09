# 05 — Interview Guide

## Question: Walk me through your pipeline.

> A push or pull request triggers one GitHub Actions job on an Ubuntu runner. It installs the project and then runs a continuous series of checks. Ruff handles linting, mypy performs type checking, pytest runs unit tests, and pytest-cov measures coverage. Bandit performs SAST, pip-audit checks known dependency vulnerabilities, and Trivy scans for committed secrets. I then run a small custom privacy policy script to demonstrate policy-as-code. Trivy reviews the Kubernetes YAML as Infrastructure as Code. After the static checks, the pipeline starts FastAPI and OWASP ZAP performs a baseline DAST scan against the running service. If the application reaches the end of the workflow, Docker builds the deployable container image.

## Question: Why both SAST and DAST?

> They examine different things. SAST analyzes source code without running the application. DAST interacts with the running service over HTTP. They are complementary rather than interchangeable.

## Question: Why unit tests and coverage?

> Unit tests verify expected behavior. Coverage measures how much code those tests exercised. High coverage does not prove security or correctness, but low coverage can show that important code paths are not being tested.

## Question: Why a custom privacy check if you already have security tools?

> Generic security tools look for common weaknesses. Privacy requirements can be organization-specific. The custom script demonstrates how a privacy rule—such as avoiding hard-coded credentials or printing full request objects—can be translated into a machine-executable pipeline check.

## Question: What is IaC?

> Infrastructure as Code means deployment infrastructure is defined in code, such as Kubernetes YAML or Terraform. Because it is code, it can be version-controlled, reviewed, and automatically scanned before deployment.

## Question: Why Docker?

> Docker packages the application and runtime dependencies into a consistent image. That image becomes the unit that can later be deployed to environments such as Kubernetes.

## Question: Where does Kubernetes fit?

> Kubernetes comes after packaging. Docker produces the image; Kubernetes manages running containerized workloads, including replicas, services, health probes, and recovery.

## Question: Is this production-ready?

> No. It is intentionally a learning project. The workflow demonstrates the concepts with understandable controls. For production, I would harden secrets management, identity, Kubernetes security, scanner thresholds, image publishing/signing, runtime monitoring, network controls, and deployment approvals.

## Question: Why are some scans non-blocking?

> A mature DevSecOps rollout often starts with visibility. Scanner findings need triage and tuning before enforcement so developers are not blocked by noise. Once policies and thresholds are agreed, high-confidence findings can become blocking gates.

## Best 90-second project explanation

> I created a very small FastAPI application so the main focus could be the delivery and privacy-control workflow. The API has a health endpoint, a simple redaction capability, and a pseudonymization example. When code changes, GitHub Actions runs one continuous job. It begins with code quality and correctness through Ruff, mypy, pytest, and coverage. It then moves into security with Bandit SAST, dependency auditing, and secret scanning. I added a custom privacy policy check to show how privacy requirements can become executable controls. Kubernetes YAML provides the Infrastructure-as-Code example and is scanned before deployment. The pipeline then starts the real FastAPI service and OWASP ZAP performs DAST against it. Finally, Docker builds the container image. The project helped me connect software engineering, DevSecOps, privacy engineering, containers, and Kubernetes in one simple lifecycle.
