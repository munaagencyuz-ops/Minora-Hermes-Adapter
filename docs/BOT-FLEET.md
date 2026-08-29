# Bot Fleet

Persistent Bots isolate responsibility; the Control Plane authorizes work.

| Profile | Model role | Enabled Minora skill | Responsibility |
|---|---|---|---|
| minora-coordinator | reasoning | none | user dialogue, calls control-plane tools, dispatches authorized work |
| minora-tender-intake | reasoning | tender-rfp-intake-builder | tender extraction and BidDecision artifact |
| minora-brief | worker | campaign-brief-builder | structured brief only |
| minora-context | worker | campaign-context-builder | company/product/market truth only |
| minora-competitor | worker | competitor-intelligence-builder | competitor evidence only |
| minora-strategy | reasoning | campaign-communication-strategy-builder | strategy only |
| minora-revision | reasoning | strategy-revision-agent | versioned revision only |

## Capability isolation

- Coordinator has control-plane tools but no domain skill.
- Each specialist has exactly one owning skill.
- Specialists cannot dispatch downstream Minora stages.
- `tender-response-builder` is not enabled until it exists as an executable canonical skill.
- Hermes memory stores preferences/procedure, not material business facts.

## Model configuration

Model names are deployment configuration, not architecture truth. Record requested and actual model IDs and fallback reasons. Vertex credentials stay outside this repository.
