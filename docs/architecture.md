# Architecture

```mermaid
flowchart TD
    D[Developer] --> G[GitHub Pull Request]
    G --> CI[CI Pipeline]
    CI --> T[Tests / Ruff / mypy]
    CI --> S[SAST / Dependency / Secret Scan]
    CI --> P[Privacy Policy Check]
    CI --> I[IaC Scan]
    T --> B[Docker Build]
    S --> B
    P --> B
    I --> B
    B --> V[Container Scan]
    V --> R[Container Registry]
    R --> K[Kubernetes]
    K --> F[FastAPI Pods]
    F --> U[Users / Calling Services]
```

## Runtime layering

```text
Kubernetes
   -> Pod
      -> Container image
         -> Ubuntu userspace
            -> Python
               -> FastAPI
```

Modern Kubernetes normally uses a CRI runtime such as containerd; Docker is still
commonly used to build/test OCI container images.
