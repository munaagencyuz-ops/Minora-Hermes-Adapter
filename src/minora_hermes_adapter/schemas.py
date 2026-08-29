def tool_schema(name: str, description: str, parameters: dict) -> dict:
    return {"name": name, "description": description, "parameters": parameters}


PROJECT_START = tool_schema(
    "minora_project_start",
    "Start a Minora project and bind the actual Hermes session to it.",
    {
        "type": "object",
        "properties": {
            "project_id": {"type": "string", "minLength": 1},
            "title": {"type": "string", "minLength": 1},
            "workflow_id": {"type": "string", "enum": ["campaign-v1", "tender-v1"]},
        },
        "required": ["project_id", "title", "workflow_id"],
        "additionalProperties": False,
    },
)

STATE_GET = tool_schema(
    "minora_state_get",
    "Read deterministic Minora project state, pending gate, and audit summary.",
    {
        "type": "object",
        "properties": {"project_id": {"type": "string", "minLength": 1}},
        "required": ["project_id"],
        "additionalProperties": False,
    },
)

ARTIFACT_REGISTER = tool_schema(
    "minora_artifact_register",
    "Register a durable artifact locator and compute its current SHA-256.",
    {
        "type": "object",
        "properties": {
            "project_id": {"type": "string", "minLength": 1},
            "skill_id": {"type": "string", "minLength": 1},
            "locator": {"type": "string", "minLength": 1},
            "schema_version": {"type": ["string", "null"]},
            "metadata": {"type": "object"},
        },
        "required": ["project_id", "skill_id", "locator"],
        "additionalProperties": False,
    },
)

ARTIFACT_VALIDATE = tool_schema(
    "minora_artifact_validate",
    "Run the canonical Minora-Skills validator and record a SHA-bound validation attestation.",
    {
        "type": "object",
        "properties": {
            "project_id": {"type": "string", "minLength": 1},
            "skill_id": {"type": "string", "minLength": 1},
            "locator": {"type": "string", "minLength": 1},
            "claims": {"type": "object", "description": "Structured claims emitted by or derived from the validator, such as bid_decision."},
        },
        "required": ["project_id", "skill_id", "locator"],
        "additionalProperties": False,
    },
)

TRANSITION_REQUEST = tool_schema(
    "minora_transition_request",
    "Request a deterministic state transition using the caller's current project version.",
    {
        "type": "object",
        "properties": {
            "project_id": {"type": "string", "minLength": 1},
            "expected_version": {"type": "integer", "minimum": 0},
            "to_state": {"type": "string", "minLength": 1},
        },
        "required": ["project_id", "expected_version", "to_state"],
        "additionalProperties": False,
    },
)

DISPATCH_SKILL = tool_schema(
    "minora_dispatch_skill",
    "Authorize a Minora skill task, create a real Hermes Kanban task, and attach the returned runtime task ID.",
    {
        "type": "object",
        "properties": {
            "project_id": {"type": "string", "minLength": 1},
            "skill_id": {"type": "string", "minLength": 1},
            "assignee_profile": {"type": "string", "minLength": 1},
            "assignee_role": {"type": "string", "minLength": 1},
            "title": {"type": "string", "minLength": 1},
            "body": {"type": "string"},
            "upstream_artifact_ids": {"type": "array", "items": {"type": "string"}},
            "expected_output_type": {"type": ["string", "null"]},
            "idempotency_key": {"type": "string", "minLength": 1},
        },
        "required": [
            "project_id", "skill_id", "assignee_profile", "assignee_role", "title",
            "upstream_artifact_ids", "idempotency_key"
        ],
        "additionalProperties": False,
    },
)

UNBLOCK_TASK = tool_schema(
    "minora_unblock_task",
    "Authorize an unblock in Minora and then call the real Hermes kanban_unblock tool.",
    {
        "type": "object",
        "properties": {
            "project_id": {"type": "string", "minLength": 1},
            "task_intent_id": {"type": "string", "minLength": 1},
        },
        "required": ["project_id", "task_intent_id"],
        "additionalProperties": False,
    },
)
