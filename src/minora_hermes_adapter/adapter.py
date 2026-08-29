from __future__ import annotations

import json
from typing import Any

from .gate_intent import parse_gate_decision
from .ports import ControlPlanePort
from .runtime import HermesKanbanRuntime


class HermesMinoraAdapter:
    def __init__(self, ctx: Any, control_plane: ControlPlanePort, validator_runner: Any | None = None) -> None:
        self.ctx = ctx
        self.control_plane = control_plane
        self.validator_runner = validator_runner
        self.kanban = HermesKanbanRuntime(ctx)

    def project_start(self, args: dict[str, Any], **kwargs: Any) -> str:
        session_id = self._require_session(kwargs)
        project = self.control_plane.start_project(args["project_id"], args["title"], args["workflow_id"])
        self.control_plane.bind_session(session_id, args["project_id"])
        return json.dumps({"ok": True, "project": project, "session_id": session_id})

    def state_get(self, args: dict[str, Any], **kwargs: Any) -> str:
        return json.dumps({"ok": True, "snapshot": self.control_plane.snapshot(args["project_id"])}, default=str)

    def artifact_register(self, args: dict[str, Any], **kwargs: Any) -> str:
        artifact = self.control_plane.register_artifact(
            args["project_id"],
            args["skill_id"],
            args["locator"],
            args.get("schema_version"),
            args.get("metadata"),
        )
        return json.dumps({"ok": True, "artifact": artifact}, default=str)

    def artifact_validate(self, args: dict[str, Any], **kwargs: Any) -> str:
        if self.validator_runner is None:
            raise RuntimeError("Validator runner is not configured")
        result = self.validator_runner.run(args["skill_id"], args["locator"])
        attestation = self.control_plane.attest_validation(
            args["project_id"],
            args["skill_id"],
            result["passed"],
            result["validator_id"],
            result["exit_code"],
            result["validated_sha256"],
            args.get("claims", {}),
        )
        return json.dumps({"ok": True, "validation": result, "artifact": attestation}, default=str)

    def transition_request(self, args: dict[str, Any], **kwargs: Any) -> str:
        project = self.control_plane.request_transition(args["project_id"], args["expected_version"], args["to_state"])
        return json.dumps({"ok": True, "project": project}, default=str)

    def dispatch_skill(self, args: dict[str, Any], **kwargs: Any) -> str:
        intent = self.control_plane.authorize_task(
            args["project_id"],
            args["skill_id"],
            args["assignee_role"],
            list(args.get("upstream_artifact_ids", [])),
            args.get("expected_output_type"),
            args["idempotency_key"],
        )
        body = self._task_body(args, intent)
        runtime_task_id = self.kanban.create_task(
            title=args["title"],
            assignee=args["assignee_profile"],
            body=body,
            project_id=args["project_id"],
            skill_id=args["skill_id"],
            idempotency_key=intent["task_intent_id"],
        )
        dispatched = self.control_plane.attach_runtime_task(
            intent["task_intent_id"],
            "hermes-kanban",
            runtime_task_id,
        )
        return json.dumps({"ok": True, "task_intent": dispatched, "runtime_task_id": runtime_task_id}, default=str)

    def unblock_task(self, args: dict[str, Any], **kwargs: Any) -> str:
        intent = self.control_plane.authorize_unblock(args["project_id"], args["task_intent_id"])
        self.kanban.unblock_task(intent["runtime_task_id"])
        return json.dumps({"ok": True, "runtime_task_id": intent["runtime_task_id"]})

    def pre_llm_call(self, *, session_id: str, user_message: str, **kwargs: Any) -> str:
        """Called only for actual inbound user turns by Hermes. Model output never enters here."""
        try:
            event = self.control_plane.record_user_event(session_id, user_message, source="actual_user_turn")
        except Exception as exc:
            if getattr(exc, "code", None) == "missing_project_binding":
                return "[Minora: no active project is bound to this session]"
            raise
        snapshot = self.control_plane.snapshot(event["project_id"])
        pending = snapshot.get("pending_gate")
        if pending:
            parsed = parse_gate_decision(pending["gate_type"], user_message)
            if parsed:
                self.control_plane.resolve_gate(
                    event["project_id"],
                    parsed.gate_type,
                    event["user_event_id"],
                    parsed.decision,
                )
        return f"[Minora project={event['project_id']}]"

    def _require_session(self, kwargs: dict[str, Any]) -> str:
        session_id = kwargs.get("session_id")
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("Hermes session_id is required")
        return session_id

    def _task_body(self, args: dict[str, Any], intent: dict[str, Any]) -> str:
        payload = {
            "task_intent_id": intent["task_intent_id"],
            "project_id": args["project_id"],
            "skill_id": args["skill_id"],
            "upstream_artifact_ids": args.get("upstream_artifact_ids", []),
            "expected_output_type": intent.get("expected_output_type"),
            "instructions": args.get("body", ""),
            "forbidden": ["Do not start downstream skills", "Do not infer missing upstream artifacts"],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
