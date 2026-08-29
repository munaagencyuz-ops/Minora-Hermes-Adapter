import json
import pytest

from minora_hermes_adapter.adapter import HermesMinoraAdapter
from minora_hermes_adapter.errors import AdapterError
from tests.fakes import FakeContext, FakeControlPlane


def dispatch_args():
    return {
        "project_id": "p1",
        "skill_id": "campaign-brief-builder",
        "assignee_profile": "minora-brief",
        "assignee_role": "brief",
        "title": "Build brief",
        "body": "Use source attachments",
        "upstream_artifact_ids": [],
        "expected_output_type": "StructuredCampaignBrief",
        "idempotency_key": "p1:brief:v1",
    }


def test_dispatch_calls_actual_hermes_kanban_schema_and_attaches_real_id():
    ctx = FakeContext()
    cp = FakeControlPlane()
    adapter = HermesMinoraAdapter(ctx, cp)

    result = json.loads(adapter.dispatch_skill(dispatch_args()))

    assert result["runtime_task_id"] == "hermes-task-123"
    assert cp.attached == [("intent-1", "hermes-kanban", "hermes-task-123")]
    name, args = ctx.dispatched[0]
    assert name == "kanban_create"
    assert set(args) == {"title", "assignee", "body", "project", "skills", "idempotency_key"}
    assert args["assignee"] == "minora-brief"
    assert args["project"] == "p1"
    assert args["skills"] == ["campaign-brief-builder"]


def test_missing_runtime_task_id_never_attaches_intent():
    ctx = FakeContext(create_result='{"ok": true}')
    cp = FakeControlPlane()
    adapter = HermesMinoraAdapter(ctx, cp)

    with pytest.raises(AdapterError) as exc:
        adapter.dispatch_skill(dispatch_args())
    assert exc.value.code == "runtime_task_id_missing"
    assert cp.attached == []


def test_unblock_calls_real_hermes_tool():
    ctx = FakeContext()
    cp = FakeControlPlane()
    adapter = HermesMinoraAdapter(ctx, cp)

    adapter.unblock_task({"project_id": "p1", "task_intent_id": "intent-1"})
    assert ctx.dispatched[-1] == ("kanban_unblock", {"task_id": "hermes-task-123"})
