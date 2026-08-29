# Minora Hermes Adapter Design

## Goal

Implement a thin, version-pinned Hermes adapter that exposes complete tool schemas, binds real sessions, dispatches real Kanban tasks through `ctx.dispatch_tool`, and delegates all workflow authority to Minora-Control-Plane.

## Decisions

- Adapter-facing fields differ from built-in Hermes fields and are translated explicitly.
- A real runtime task ID is mandatory.
- Strict deterministic phrases resolve human gates.
- Raw Kanban creation is not a second Minora path.
- Unit and contract tests are distinct from live E2E.
- Hermes version compatibility is explicit and tested.
