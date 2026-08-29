from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import subprocess
import sys

from .errors import AdapterError


@dataclass(frozen=True)
class ValidatorSpec:
    validator_id: str
    relative_path: str
    input_flag: str


DEFAULT_VALIDATORS: dict[str, ValidatorSpec] = {
    "tender-rfp-intake-builder": ValidatorSpec("validate_tender.py", "tender-rfp-intake-builder/scripts/validate_tender.py", "--tender"),
    "campaign-brief-builder": ValidatorSpec("validate_brief.py", "campaign-brief-builder/scripts/validate_brief.py", "--brief"),
    "campaign-context-builder": ValidatorSpec("validate_context.py", "campaign-context-builder/scripts/validate_context.py", "--context"),
    "competitor-intelligence-builder": ValidatorSpec("validate_intelligence.py", "competitor-intelligence-builder/scripts/validate_intelligence.py", "--campaign"),
    "campaign-communication-strategy-builder": ValidatorSpec("validate_strategy.py", "campaign-communication-strategy-builder/scripts/validate_strategy.py", "--strategy"),
    "strategy-revision-agent": ValidatorSpec("validate_revision.py", "strategy-revision-agent/scripts/validate_revision.py", "--revision"),
}


class SkillValidatorRunner:
    def __init__(self, skills_root: str | Path) -> None:
        self.skills_root = Path(skills_root)

    def run(self, skill_id: str, locator: str) -> dict:
        try:
            spec = DEFAULT_VALIDATORS[skill_id]
        except KeyError as exc:
            raise AdapterError("validator_not_configured", f"No canonical validator configured for {skill_id}") from exc
        validator = self.skills_root / spec.relative_path
        artifact = Path(locator.removeprefix("file://"))
        if not validator.is_file():
            raise AdapterError("validator_missing", str(validator))
        if not artifact.is_file():
            raise AdapterError("artifact_missing", str(artifact))
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        proc = subprocess.run(
            [sys.executable, str(validator), spec.input_flag, str(artifact)],
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "passed": proc.returncode == 0,
            "validator_id": spec.validator_id,
            "exit_code": proc.returncode,
            "validated_sha256": digest,
            "stdout_summary": proc.stdout[:1000],
            "stderr_summary": proc.stderr[:1000],
        }
