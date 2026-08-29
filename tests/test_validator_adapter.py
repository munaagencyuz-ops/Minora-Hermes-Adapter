import json

from minora_hermes_adapter.adapter import HermesMinoraAdapter
from tests.fakes import FakeContext, FakeControlPlane


class FakeRunner:
    def run(self, skill_id, locator):
        return {
            "passed": True,
            "validator_id": "validate_brief.py",
            "exit_code": 0,
            "validated_sha256": "a" * 64,
            "stdout_summary": "PASS",
            "stderr_summary": "",
        }


def test_artifact_validate_records_attestation():
    cp = FakeControlPlane()
    adapter = HermesMinoraAdapter(FakeContext(), cp, FakeRunner())
    result = json.loads(adapter.artifact_validate({
        "project_id": "p1",
        "skill_id": "campaign-brief-builder",
        "locator": "/tmp/brief.json",
        "claims": {},
    }))
    assert result["ok"] is True
    assert result["artifact"]["validation_status"] == "passed"
