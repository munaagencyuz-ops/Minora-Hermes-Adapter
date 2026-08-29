# Minora Hermes Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Execute task-by-task.

**Goal:** Build and verify the Hermes runtime adapter without duplicating Minora policy.

**Architecture:** Complete model-facing tools call the public Control Plane. Authorized task intents are translated into actual Hermes Kanban calls via `ctx.dispatch_tool`; real returned IDs are attached back to the Control Plane.

**Tech Stack:** Python 3.11+, Hermes plugin API, pytest, Google Vertex deployment configuration.

**Spec:** `docs/superpowers/specs/2026-08-29-minora-hermes-adapter-design.md`

## Global Constraints

- No fake task IDs.
- No invented Hermes arguments.
- No duplicated control-plane policy.
- No fixture-only live claim.
- No credentials in source control.

### Task 1: Plugin registration and schemas

- [ ] Install against the pinned Hermes build.
- [ ] Verify every model-facing schema is non-empty and has required fields.
- [ ] Verify PluginManager discovers the plugin.
- [ ] Run `pytest tests/test_plugin_registration.py -q`.
- [ ] Commit with `feat: register versioned Minora Hermes tools`.

### Task 2: Real Kanban dispatch

- [ ] Verify wrapper sends `title`, `assignee`, `body`, `project`, `skills`, and `idempotency_key`.
- [ ] Verify missing runtime task ID returns failure and never attaches the intent.
- [ ] Verify unblock calls the real `kanban_unblock` schema.
- [ ] Run `pytest tests/test_kanban_runtime.py -q`.
- [ ] Commit with `feat: dispatch authorized work to real Hermes Kanban`.

### Task 3: Session and gate events

- [ ] Verify project start binds the callback's actual session ID.
- [ ] Verify only exact user phrases resolve the current gate.
- [ ] Verify assistant text and mixed messages do not resolve gates.
- [ ] Run `pytest tests/test_gate_hook.py -q`.
- [ ] Commit with `feat: map real Hermes user turns to Minora gates`.

### Task 4: Bot fleet and compatibility

- [ ] Apply profile templates with one owning skill per specialist.
- [ ] Verify coordinator has no domain skill and no raw Minora bypass.
- [ ] Verify requested and actual Vertex model IDs.
- [ ] Run real plugin/Kanban smoke checks.
- [ ] Commit with `chore: add Hermes profile and compatibility verification`.

### Task 5: Live E2E and release

- [ ] Use source documents absent from repository fixtures.
- [ ] Capture real TaskIntent and Hermes task IDs.
- [ ] Capture generated artifact, validator, SHA, gate, and user event.
- [ ] Verify no unsupported facts were invented.
- [ ] Publish fresh CI and live-E2E evidence on the exact release SHA.
