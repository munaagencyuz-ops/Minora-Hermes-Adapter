from minora_hermes_adapter import plugin
from tests.fakes import FakeContext, FakeControlPlane


class FakeValidatorRunner:
    pass


def test_all_registered_tools_have_complete_model_facing_schemas(monkeypatch):
    ctx = FakeContext()
    monkeypatch.setattr(plugin, "build_control_plane", lambda: FakeControlPlane())
    monkeypatch.setattr(plugin, "SkillValidatorRunner", lambda root: FakeValidatorRunner())
    monkeypatch.setenv("MINORA_SKILLS_ROOT", "/tmp/minora-skills")
    plugin.register(ctx)

    assert ctx.tools
    for tool in ctx.tools:
        schema = tool["schema"]
        assert schema["name"] == tool["name"]
        assert isinstance(schema["description"], str) and schema["description"]
        params = schema["parameters"]
        assert params["type"] == "object"
        assert "properties" in params
        assert params.get("additionalProperties") is False
    assert any(name == "pre_llm_call" for name, _ in ctx.hooks)
