# Live End-to-End Test

## Definition

A live E2E test must use all of the following:

- a real Hermes process;
- the actual `minora-coordinator` profile;
- the installed adapter plugin discovered by PluginManager;
- the configured control-plane database;
- real Hermes Kanban creation and a real task ID;
- the actual specialist Bot/Profile;
- new source documents not copied from the expected TenderIntake fixture;
- a newly generated artifact;
- the owning Minora-Skills validator;
- a real inbound human confirmation event.

A Python script that imports plugin functions and feeds a known JSON fixture is an integration test, not live E2E.

## Tender E2E acceptance trace

Capture:

1. Hermes session ID;
2. Minora project ID;
3. session binding;
4. source attachment IDs and hashes;
5. detection decision;
6. TaskIntent ID;
7. real Hermes Kanban task ID;
8. assignee profile;
9. skill ID and loaded canonical skill path;
10. newly generated TenderIntake locator and SHA;
11. validator command, exit code, and validated SHA;
12. BidDecision;
13. created human gate;
14. real user event ID and non-empty message hash;
15. gate resolution;
16. allowed next action.

## Anti-leakage test

The new source set must not appear in repository fixtures. A reviewer must compare the generated artifact with the source documents and confirm no unsupported audience, competitor, channel, KPI, USP, media budget, winning price, or win probability was invented.

## Reporting language

Use `live_e2e_status: passed` only when the real runtime evidence above is attached. Otherwise use `not_run`, `blocked`, or `failed`.
