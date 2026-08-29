# Hermes v0.19 Compatibility Contract

Pinned reference: Hermes Agent v0.19.x. Re-verify against the exact installed build before release.

## Plugin structure

```text
plugin.yaml
__init__.py  # exposes register(ctx)
```

The installed package may keep implementation modules elsewhere, but there must be one canonical implementation.

## Stable public APIs used

- `ctx.register_tool(...)`
- `ctx.register_hook(...)`
- `ctx.dispatch_tool(name, args)`
- `ctx.profile_name`

Do not use private `_cli_ref` state.

## Model-facing tool schema

Every registered plugin tool schema must have the full Hermes/OpenAI shape: `name`, model-facing `description`, and `parameters`. A bare `{type, properties}` object is not sufficient.

## Built-in Kanban contract used by this adapter

`kanban_create` uses the actual Hermes fields:

```text
title       required
assignee    required
body
parents
project
skills
idempotency_key
model
provider
```

It does not use invented fields such as `assignee_profile` or `metadata` when calling the built-in tool. Those are adapter-facing fields only and are translated before dispatch.

`kanban_unblock` uses:

```text
task_id     required
board       optional
```

## Hook assumptions

`pre_llm_call` is treated as an inbound user-turn hook only if the installed Hermes version confirms that behavior. The compatibility test must inspect the actual callback payload and must not synthesize a model message through the same path.

## Upgrade rule

When Hermes changes:

1. run schema compatibility tests;
2. run plugin registration smoke test;
3. run actual Kanban create/unblock smoke test;
4. run one new-source live E2E;
5. update the supported version range only after all pass.
