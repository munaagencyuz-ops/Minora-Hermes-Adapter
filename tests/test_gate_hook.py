from minora_hermes_adapter.adapter import HermesMinoraAdapter
from tests.fakes import FakeContext, FakeControlPlane


def test_exact_user_phrase_resolves_current_gate():
    cp = FakeControlPlane()
    cp.pending_gate = {"gate_type": "brief_confirmation"}
    adapter = HermesMinoraAdapter(FakeContext(), cp)

    adapter.pre_llm_call(session_id="s1", user_message="ПОДТВЕРЖДАЮ БРИФ")

    assert len(cp.user_events) == 1
    assert cp.resolutions == [("p1", "brief_confirmation", "uevt-1", "confirmed")]


def test_agent_like_or_mixed_text_does_not_resolve_gate():
    cp = FakeControlPlane()
    cp.pending_gate = {"gate_type": "brief_confirmation"}
    adapter = HermesMinoraAdapter(FakeContext(), cp)

    adapter.pre_llm_call(session_id="s1", user_message="I confirmed the brief for the user")
    adapter.pre_llm_call(session_id="s1", user_message="ПОДТВЕРЖДАЮ БРИФ, но поменяй бюджет")

    assert cp.resolutions == []
