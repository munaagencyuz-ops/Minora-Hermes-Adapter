# Adapter Conformance

Passing `pytest` proves only adapter contract behavior against fakes. It does not prove Hermes is installed, the plugin is loaded, Kanban dispatched work, a profile ran, or source documents were processed.

## Release gates

### Contract gate

- all model-facing schemas have `name`, `description`, and `parameters`;
- handlers accept `**kwargs` for Hermes v0.19 dispatch compatibility;
- `ctx.dispatch_tool("kanban_create", ...)` receives only real Hermes fields;
- the real returned task ID is attached to a Control Plane TaskIntent;
- a missing/failed runtime result cannot become success;
- `kanban_unblock` uses the real `task_id` contract.

### Runtime smoke gate

Run against the exact installed Hermes build and attach evidence for plugin discovery, visible tools, real Kanban create/unblock, and worker profile execution.

### Live E2E gate

Use new source documents absent from fixtures and capture the complete trace in `docs/LIVE-E2E.md`. The release status must remain `contract_verified` until this gate passes.
