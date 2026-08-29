from __future__ import annotations

from .adapter import HermesMinoraAdapter
from .factory import build_control_plane
from .validator import SkillValidatorRunner
import os
from . import schemas


def register(ctx):
    adapter = HermesMinoraAdapter(ctx, build_control_plane(), SkillValidatorRunner(os.environ["MINORA_SKILLS_ROOT"]))

    ctx.register_tool("minora_project_start", "minora", schemas.PROJECT_START, adapter.project_start, description="Start a Minora project and bind the actual Hermes session")
    ctx.register_tool("minora_state_get", "minora", schemas.STATE_GET, adapter.state_get, description="Read deterministic Minora state")
    ctx.register_tool("minora_artifact_register", "minora", schemas.ARTIFACT_REGISTER, adapter.artifact_register, description="Register a Minora artifact")
    ctx.register_tool("minora_artifact_validate", "minora", schemas.ARTIFACT_VALIDATE, adapter.artifact_validate, description="Run the canonical skill validator and record a SHA-bound attestation")
    ctx.register_tool("minora_transition_request", "minora", schemas.TRANSITION_REQUEST, adapter.transition_request, description="Request a deterministic Minora transition")
    ctx.register_tool("minora_dispatch_skill", "minora", schemas.DISPATCH_SKILL, adapter.dispatch_skill, description="Authorize and create a real Hermes Kanban task for a Minora skill")
    ctx.register_tool("minora_unblock_task", "minora", schemas.UNBLOCK_TASK, adapter.unblock_task, description="Authorize and call the real Hermes Kanban unblock tool")
    ctx.register_hook("pre_llm_call", adapter.pre_llm_call)
