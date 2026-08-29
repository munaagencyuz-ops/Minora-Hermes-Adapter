from __future__ import annotations

import json
from typing import Any

from .errors import AdapterError


def parse_tool_result(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict):
        result = raw
    elif isinstance(raw, str):
        try:
            result = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AdapterError("runtime_result_not_json", "Hermes tool returned non-JSON output") from exc
    else:
        raise AdapterError("runtime_result_invalid", f"Unsupported Hermes tool result type: {type(raw)!r}")
    if result.get("ok") is False or result.get("success") is False:
        raise AdapterError("runtime_tool_failed", str(result))
    return result


class HermesKanbanRuntime:
    """Uses the public PluginContext.dispatch_tool API and actual Hermes Kanban fields."""

    def __init__(self, ctx: Any) -> None:
        self.ctx = ctx

    def create_task(
        self,
        *,
        title: str,
        assignee: str,
        body: str,
        project_id: str,
        skill_id: str,
        idempotency_key: str,
    ) -> str:
        raw = self.ctx.dispatch_tool(
            "kanban_create",
            {
                "title": title,
                "assignee": assignee,
                "body": body,
                "project": project_id,
                "skills": [skill_id],
                "idempotency_key": idempotency_key,
            },
        )
        result = parse_tool_result(raw)
        task_id = result.get("task_id") or result.get("id")
        if not isinstance(task_id, str) or not task_id.strip():
            raise AdapterError("runtime_task_id_missing", "Hermes kanban_create returned no real task ID")
        return task_id

    def unblock_task(self, task_id: str) -> None:
        raw = self.ctx.dispatch_tool("kanban_unblock", {"task_id": task_id})
        parse_tool_result(raw)
