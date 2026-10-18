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

## Reusable base components: uncontrolled is built ON TOP OF controlled

Every reusable BASE component that holds interaction state (dropdown, stepper,
tabs, toggler, accordion, ...) must be implemented from its controlled version:
the controlled API (`value` + `onValueChange`-style props) is the core, and the
uncontrolled mode is only a thin layer that owns state and feeds that same
core. The standard shape is hybrid props — optional `value`/`onValueChange`
with an internal-state fallback when they're omitted. Never ship an
uncontrolled-only base component.

- Why: uncontrolled-only dead-ends real needs — programmatic jumps, async
  flows that advance on resolve, deep-linking, resets, state lifted for
  persistence — and retrofitting control later is a breaking change, while the
  controlled core costs nothing up front.
- Exception: SPECIFIC components composed from base components (a ViewToggler
  built on a TogglerButton, an app form built on inputs) may be
  uncontrolled-only — they delegate state to their base pieces.
- Applies to every project, and flag violations when touching existing base
  components.

## "Step by step" means one step at a time

When I ask for step-by-step guidance, give me **exactly one step**, then stop and ask
whether to continue before giving the next one. Don't dump the whole sequence.

- This is guidance I'm going to *perform*, so I need to do step one and see what
  actually happened before step two is even the right step. A full list assumes an
  outcome for every step that hasn't happened yet.
- **One step means one thing to do.** If a step has parts — open this menu, then fill
  that field, then click Upload — those are steps too. Give me the first part, wait,
  then the next. Never hand me a list of parts to hold in my head; I have very little
  working memory, and a five-part step is five things I've been asked to remember.
- Each part still arrives complete: what to do, what I should see when it worked, and
  what to do if it didn't. Small unit, not a thin one.
- Wait for me to say continue. If what I report back changes the plan, adjust the
  remaining steps rather than proceeding with the original next one.
- Applies whatever the medium — chat, an artifact, a file. If a written record of the
  whole sequence is genuinely useful, ask first, and still walk me through it one step
  at a time.
- It does not apply when I ask you to *do* the work yourself; then just do all of it.

## Commands I must run myself: show first, then ask before copying to the clipboard

When you hand me a command to execute in my own terminal, (1) show it in the
reply, (2) say you're going to copy it to the clipboard, and (3) **wait for my
explicit yes** before running `pbcopy`. Never write to the clipboard unasked.

- Why: I often hold something I still need in the clipboard (an API key I just
  generated and haven't pasted yet, for example). A silent `pbcopy` overwrites
  it and I lose it — and a one-time secret means regenerating it.
- Applies to every project and every medium. "Copy this" from me in the same
  message counts as the yes.
