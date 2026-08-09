# Kubernetes Notes

This folder demonstrates deployment controls an interviewer may ask about:

- Multiple replicas / desired state
- Liveness and readiness probes
- Non-root execution
- No privilege escalation
- Read-only root filesystem
- Dropped Linux capabilities
- Resource requests and limits
- Service abstraction
- NetworkPolicy
- Secrets referenced by name rather than committed to Git
- Disabled automatic service-account-token mounting

Before deployment, replace the image placeholder and create `privacy-demo-secrets`
from an approved secret-management workflow. Do **not** commit the real Secret values.
