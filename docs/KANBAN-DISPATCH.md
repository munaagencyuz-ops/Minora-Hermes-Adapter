# Real Kanban Dispatch

## Correct sequence

```text
minora_dispatch_skill
  1. Control Plane authorize_task(...)
  2. ctx.dispatch_tool("kanban_create", actual Hermes args)
  3. parse actual response
  4. require real task_id
  5. Control Plane attach_runtime_task(...)
```

## Invalid sequence

```text
generate local task_0001
write audit row
return success
```

That creates no Hermes work and is forbidden.

## Task body

The task body contains a machine-readable envelope:

- task_intent_id;
- project_id;
- skill_id;
- exact upstream artifact IDs;
- expected output type;
- instructions;
- explicit prohibition on downstream execution.

## Completion

The worker must provide a structured handoff. The adapter must verify:

- runtime task ID matches the recorded TaskIntent;
- output artifact exists;
- output skill ID matches the task;
- validator result is recorded against the current SHA;
- task completion does not itself authorize the next stage.

## Unblock

`minora_unblock_task` first asks the Control Plane. Only then does it call `ctx.dispatch_tool("kanban_unblock", {"task_id": ...})`.
