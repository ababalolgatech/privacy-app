# Mini Privacy / Security Threat Model

| Asset / Flow | Threat | Example Impact | Demo Control |
|---|---|---|---|
| API credential | Secret committed to Git | Unauthorized API use | Secret scan + Kubernetes secret reference |
| Raw member identifier | Logged in plaintext | PII/PHI leakage into log platform | Metadata-only logging + redacting formatter + test |
| Tokenization key | Embedded in image | Re-identification / token compromise | Runtime environment secret + production fail-closed check |
| API endpoint | Missing auth | Unauthorized processing | `X-API-Key` demo dependency |
| Docker image | Vulnerable package | Application compromise | Trivy image scan |
| Cloud/K8s config | Privileged workload | Container escape / increased blast radius | Non-root, drop capabilities, no privilege escalation |
| Service network | Unrestricted communication | Lateral movement | NetworkPolicy example |
| Dependency | Known CVE | Exploitation | `pip-audit` + Dependabot |
| Source code | Security defect | Injection / unsafe logic | Bandit + CodeQL + review |
| Release | Untested change | Production defect | CI quality gates and coverage threshold |

## Privacy questions to discuss in an interview

1. Is HMAC tokenization sufficient for the business use case, or is a reversible token vault required?
2. Should the service ever support detokenization? If yes, how should that privilege be isolated and audited?
3. What data classification applies to the input and token?
4. How long should audit records be retained?
5. Which systems are allowed to call this API?
6. Could the purpose field itself contain PII and therefore require validation/redaction?
7. How should keys be rotated without breaking existing tokens?
