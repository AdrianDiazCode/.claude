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

## Compose components of components — inline maps and repeated markup are extraction signals

Avoid repetition in UI code; favor sensible abstractions. Build components by composing
smaller components rather than accumulating inline markup.

- A `.map()` whose body renders more than a trivial line of JSX is a strong clue that
  the body should be its own component. The same goes for long inline conditional
  blocks and for near-identical markup appearing in more than one place — that must be
  one shared component, not parallel copies.
- Before writing a new component, check whether an existing one (project or shared
  library) already fits or can be composed.
- When extracting, prefer a generic reusable shape (title/children-style props) and
  keep the use-case-specific formatting at the call site.
- Apply this when writing new UI and flag it when touching existing code that violates it.

## Every backend logic bug fix ships with a regression test

When fixing a bug in backend logic (a wrong query, calculation, state transition,
authorization check, ...), always add a test in the repo's existing suite that
reproduces the failure — not just the fix. The bug existing means the current suite
didn't cover that case.

- The test must assert the observable behavior that was wrong (e.g. "a fully paid
  contract reports no debt"), not the implementation detail, so it survives refactors.
- **Prove it catches the bug**: run it once with the bug temporarily reintroduced and
  confirm it fails, then restore the fix and confirm the full suite passes.
- Also cover the inverse/boundary case when cheap, so the fix can't overcorrect
  (e.g. real debt is still reported).
- Follow the repo's existing test conventions (level, fixtures, naming); don't invent
  a new harness for one test.
