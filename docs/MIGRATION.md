# Migration from the Minora-Skills Hermes Plugin

1. Install and verify Minora-Control-Plane.
2. Install this adapter and run contract tests.
3. Configure Bots and the adapter against the same Minora-Skills registry version.
4. Run a real Hermes Kanban create/unblock smoke test.
5. Run a new-source tender live E2E.
6. Remove `.hermes/plugins/minora-orchestrator` from Minora-Skills.
7. Remove runtime/orchestrator tests from Minora-Skills after equivalent tests pass here.
8. Update cross-repository documentation.
9. Keep no duplicate implementation or compatibility shadow copy.
