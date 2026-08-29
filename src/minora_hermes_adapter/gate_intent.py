from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateDecision:
    gate_type: str
    decision: str


_EXACT: dict[tuple[str, str], str] = {
    ("brief_confirmation", "ПОДТВЕРЖДАЮ БРИФ"): "confirmed",
    ("brief_confirmation", "CONFIRM BRIEF"): "confirmed",
    ("bid_decision_confirmation", "ПРОДОЛЖАЕМ УЧАСТИЕ"): "confirmed",
    ("bid_decision_confirmation", "PROCEED WITH BID"): "confirmed",
    ("no_go_override", "ПРОДОЛЖИТЬ НЕСМОТРЯ НА NO_GO"): "overridden",
    ("no_go_override", "OVERRIDE NO_GO"): "overridden",
    ("strategy_approval", "УТВЕРЖДАЮ СТРАТЕГИЮ"): "approved",
    ("strategy_approval", "APPROVE STRATEGY"): "approved",
}


def parse_gate_decision(pending_gate: str | None, user_message: str) -> GateDecision | None:
    """Strict deterministic parser. It intentionally rejects mixed/verbose messages."""
    if not pending_gate:
        return None
    normalized = " ".join(user_message.strip().upper().split())
    decision = _EXACT.get((pending_gate, normalized))
    return GateDecision(pending_gate, decision) if decision else None
