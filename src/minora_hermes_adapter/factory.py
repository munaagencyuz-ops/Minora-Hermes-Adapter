from __future__ import annotations

import os
from pathlib import Path


def build_control_plane():
    """Lazy import keeps contract tests independent of the sibling private repository."""
    from minora_control_plane import ControlPlane, FileHashResolver, SkillRegistry, SQLiteStore, WorkflowRegistry

    control_repo = Path(os.environ["MINORA_CONTROL_PLANE_ROOT"])
    state_db = Path(os.environ.get("MINORA_CONTROL_PLANE_DB", control_repo / "runtime" / "minora.sqlite3"))
    return ControlPlane(
        SQLiteStore(state_db),
        SkillRegistry(control_repo / "config" / "skill-registry.json"),
        WorkflowRegistry(control_repo / "config" / "workflows"),
        FileHashResolver(),
    )
