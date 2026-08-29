# Agent Instructions — Minora Hermes Adapter

Read all architecture and compatibility documents before editing.

## Hard boundaries

- Do not reimplement Minora workflow policy in this repository.
- Do not copy Minora skill prompts into the plugin.
- Do not fake Kanban task IDs.
- Do not assume Hermes tool arguments; test against the pinned Hermes contract.
- Do not call a fixture test live E2E.
- Do not use assistant/model text as a human event.
- Do not silently fall back to a `default` project.
- Do not let raw `kanban_create` become a second Minora orchestration path.
- Do not claim a Bot ran unless a real runtime task ID and completion event exist.
- Do not expose credentials in logs or reports.

## Runtime compatibility

Every release must pin and test a supported Hermes version range. If Hermes changes a hook signature or Kanban schema, the adapter must fail compatibility checks rather than guess.
