# Security Notes

- Run model tools with least privilege and explicit allow lists.
- Keep uploaded documents in object storage and scan them before parsing.
- Do not give agents unrestricted shell, network, or filesystem access.
- Add authentication at the gateway before exposing the API outside localhost.
- Log tool calls, retrieval sources, model choices, and policy decisions.
- Redact secrets before storing prompts, traces, eval samples, or failures.
