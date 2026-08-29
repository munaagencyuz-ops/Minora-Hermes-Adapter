# Minora Hermes Adapter

Hermes-specific runtime integration for the runtime-independent Minora Control Plane.

This repository owns the **Hermes plugin**, **Bot/Profile topology**, **real Kanban dispatch**, **session binding**, **tool schemas**, **Vertex templates**, **Hermes compatibility tests**, and the procedure for a genuine live end-to-end test.

It does **not** own Minora workflow policy or domain skill content.

## Repository boundary

```text
Minora-Skills           domain skills and validators
Minora-Control-Plane    deterministic policy and state
Minora-Hermes-Adapter   Hermes API translation and real runtime execution
```

## Critical rule

A wrapper called `minora_dispatch_skill` must call the real Hermes tool:

```python
ctx.dispatch_tool("kanban_create", {
    "title": ...,
    "assignee": ...,
    "body": ...,
    "project": ...,
    "skills": [...],
    "idempotency_key": ...
})
```

It may not generate its own fake `task_id`. The returned ID is attached to the Control Plane TaskIntent only after the real Hermes call succeeds.

## Test vocabulary

- Tests using `FakePluginContext` are contract tests.
- Tests using prebuilt TenderIntake JSON are fixture integration tests.
- Only a test that starts actual Hermes, loads the actual plugin/profile, invokes real Kanban, and processes new source documents is called live E2E.

## Start here

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/HERMES-V019-CONTRACT.md`](docs/HERMES-V019-CONTRACT.md)
- [`docs/BOT-FLEET.md`](docs/BOT-FLEET.md)
- [`docs/KANBAN-DISPATCH.md`](docs/KANBAN-DISPATCH.md)
- [`docs/LIVE-E2E.md`](docs/LIVE-E2E.md)
- [`docs/FAILURE-CATALOG.md`](docs/FAILURE-CATALOG.md)
- [`IMPLEMENTATION_TASK.json`](IMPLEMENTATION_TASK.json)

## Development

```bash
python -m pip install -e '.[dev]'
pytest -q
```

The unit/contract suite does not require Hermes. Live E2E requires an installed Hermes version explicitly supported by this adapter and a configured Control Plane.
