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

## Single source of truth — the most important principle

Never repeat information that can be inferred or read from somewhere else (CI scripts,
configs, code, docs). Duplicated values drift silently; derive them from the canonical
source instead. If duplication is truly unavoidable, add a check that fails when the
copies diverge.

## Short, concrete answers by default

Lead with the answer/recommendation in a few sentences. Skip exhaustive pros/cons,
headers, and adjacent findings. Expand only when explicitly asked.

## Don't encode sequences as numeric order/priority fields

Use a single ordered array of keys/ids, validated for uniqueness and exhaustiveness
against the collection — scattered numbers hide the sequence and allow duplicates. Flag
the pattern in existing code.
