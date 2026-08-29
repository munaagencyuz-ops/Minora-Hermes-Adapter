from __future__ import annotations


class FakeContext:
    def __init__(self, create_result='{"ok": true, "task_id": "hermes-task-123"}'):
        self.create_result = create_result
        self.dispatched = []
        self.tools = []
        self.hooks = []

    def dispatch_tool(self, name, args):
        self.dispatched.append((name, args))
        if name == "kanban_create":
            return self.create_result
        if name == "kanban_unblock":
            return '{"ok": true, "task_id": "hermes-task-123"}'
        raise AssertionError(name)

    def register_tool(self, name, toolset, schema, handler, description=None):
        self.tools.append({"name": name, "toolset": toolset, "schema": schema, "handler": handler, "description": description})

    def register_hook(self, name, handler):
        self.hooks.append((name, handler))


class FakeControlPlane:
    def __init__(self):
        self.attached = []
        self.user_events = []
        self.resolutions = []
        self.pending_gate = None

    def start_project(self, project_id, title, workflow_id):
        return {"project_id": project_id, "title": title, "workflow_id": workflow_id, "state": "input_received", "version": 0}

    def bind_session(self, session_id, project_id):
        self.binding = (session_id, project_id)
        return {"session_id": session_id, "project_id": project_id}

    def record_user_event(self, session_id, message, source="actual_user_turn"):
        event = {"user_event_id": f"uevt-{len(self.user_events)+1}", "project_id": "p1", "session_id": session_id, "source": source}
        self.user_events.append((event, message))
        return event

    def resolve_gate(self, project_id, gate_type, user_event_id, decision):
        self.resolutions.append((project_id, gate_type, user_event_id, decision))
        self.pending_gate = None
        return {"status": "resolved"}

    def register_artifact(self, project_id, skill_id, locator, schema_version=None, metadata=None):
        return {"artifact_id": "art-1", "project_id": project_id, "skill_id": skill_id, "locator": locator}

    def attest_validation(self, project_id, skill_id, passed, validator_id, exit_code, validated_sha256, claims=None):
        return {"artifact_id": "art-1", "project_id": project_id, "skill_id": skill_id, "validation_status": "passed" if passed else "failed", "validated_sha256": validated_sha256}

    def request_transition(self, project_id, expected_version, to_state):
        return {"project_id": project_id, "version": expected_version + 1, "state": to_state}

    def authorize_task(self, project_id, skill_id, assignee_role, upstream_artifact_ids, expected_output_type, idempotency_key):
        return {"task_intent_id": "intent-1", "project_id": project_id, "skill_id": skill_id, "assignee_role": assignee_role, "upstream_artifact_ids": upstream_artifact_ids, "expected_output_type": expected_output_type, "status": "authorized"}

    def attach_runtime_task(self, task_intent_id, runtime_system, runtime_task_id):
        self.attached.append((task_intent_id, runtime_system, runtime_task_id))
        return {"task_intent_id": task_intent_id, "runtime_task_id": runtime_task_id, "status": "dispatched"}

    def authorize_unblock(self, project_id, task_intent_id):
        return {"project_id": project_id, "task_intent_id": task_intent_id, "runtime_task_id": "hermes-task-123"}

    def snapshot(self, project_id):
        return {"project": {"project_id": project_id}, "pending_gate": self.pending_gate}
