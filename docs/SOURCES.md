# Official Hermes Sources

This adapter contract is based on official Nous Research Hermes documentation and source code. Re-check these sources for every Hermes upgrade:

- https://hermes-agent.nousresearch.com/docs/developer-guide/plugins
- https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
- https://github.com/NousResearch/hermes-agent/blob/main/hermes_cli/plugins.py
- https://github.com/NousResearch/hermes-agent/blob/main/tools/kanban_tools.py

Important v0.19 compatibility note: plugin handlers must accept `**kwargs` because runtime dispatch may pass `task_id`, `session_id`, `tool_call_id`, `turn_id`, and related context.
