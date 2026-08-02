# Global guidance for Claude Code (all projects)

## Evaluate every solution for idempotency, reproducibility, and scalability — before proposing it

Before suggesting or making any change — especially to infrastructure, data stores, or
systems — check that it is idempotent, reproducible, and scalable. Lead with the durable
solution. Do not present a one-off as the primary path.

- **Prefer declarative Infrastructure-as-Code** (Terraform, Kubernetes manifests, config
  files, migrations) over imperative one-off mutations to live resources
  (`aws … modify`, `kubectl edit`, console clicks, hand-patched policies). When a source of
  truth exists, the change goes *there first*.
- An imperative live change is acceptable **only** as an explicitly-labeled emergency
  stopgap, and it must be mirrored in the IaC source so it survives a rebuild/recreate.
  Always call out the resulting **state drift** and how it will be reconciled.
- If you mention a quick hack to unblock, mark it clearly as **temporary and secondary** —
  never as the recommended fix.
- When you deviate from the reproducible path, say so explicitly and explain the trade-off.
