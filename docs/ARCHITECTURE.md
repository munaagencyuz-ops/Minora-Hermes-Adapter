# Hermes Adapter Architecture

## Adapter role

The adapter translates Hermes events and tool calls into the public Minora Control Plane API. It contains no campaign or tender policy.

```text
Hermes inbound user turn
  → pre_llm_call
  → Control Plane record_user_event
  → strict gate-intent parser
  → Control Plane resolve_gate

Coordinator calls minora_dispatch_skill
  → Control Plane authorize_task
  → ctx.dispatch_tool("kanban_create", real Hermes arguments)
  → Hermes returns real task_id
  → Control Plane attach_runtime_task

Worker completes
  → adapter receives runtime completion event
  → artifact registered
  → Minora-Skills validator runs
  → validation attestation recorded
  → next transition requested
```

## Why the adapter cannot own policy

Hermes may be replaced. Minora rules must remain identical in a web app, API, or another agent runtime. The adapter therefore does not decide whether Context may run, whether a gate is satisfied, or whether a skill is executable. It asks the Control Plane.

## Raw Kanban access

The coordinator profile should expose `minora_dispatch_skill`, not raw `kanban_create`, for Minora work. Specialist workers may use their own lifecycle tools, but cannot create the next Minora stage.

A pre-tool hook may block obvious attempts to use raw Kanban for Minora tasks, but correctness must not depend on string heuristics. Capability configuration is the primary control: remove raw creation tools from the coordinator when possible.

## Real completion

A TaskIntent is not dispatched until Hermes returns a real task ID. A worker response in prose is not completion. The adapter must consume the real Kanban completion event and structured handoff.
