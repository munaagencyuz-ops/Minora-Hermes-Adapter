import json

from minora_hermes_adapter.adapter import HermesMinoraAdapter
from tests.fakes import FakeContext, FakeControlPlane


def test_project_start_binds_actual_callback_session():
    cp = FakeControlPlane()
    adapter = HermesMinoraAdapter(FakeContext(), cp)
    result = json.loads(adapter.project_start(
        {"project_id": "p1", "title": "Tender", "workflow_id": "tender-v1"},
        session_id="actual-hermes-session",
    ))
    assert result["ok"] is True
    assert cp.binding == ("actual-hermes-session", "p1")
