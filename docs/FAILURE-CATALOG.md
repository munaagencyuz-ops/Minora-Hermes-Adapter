# Adapter Failure Catalog

| ID | Failure | Required prevention |
|---|---|---|
| HA-01 | plugin exists but PluginManager did not load it | plugin list/doctor and real tool visibility |
| HA-02 | tools registered with empty schemas | schema contract test for every model-facing tool |
| HA-03 | adapter uses nonexistent Kanban fields | test exact dispatched payload against pinned Hermes contract |
| HA-04 | wrapper returns a generated task ID | require ID from `ctx.dispatch_tool` result |
| HA-05 | wrapper never calls real Kanban | FakeContext asserts exact dispatch call; live smoke confirms task exists |
| HA-06 | session binding only exists as an internal test helper | expose `minora_project_start` and bind real session |
| HA-07 | assistant text enters human event path | only inbound `pre_llm_call` callback accepted; exact gate parser |
| HA-08 | verbose/mixed user message accidentally confirms | exact deterministic phrase matching; otherwise ask again |
| HA-09 | raw Kanban becomes a bypass | coordinator capability isolation and wrapper-only policy |
| HA-10 | prebuilt TenderIntake is called live PDF extraction | strict test vocabulary and new-source E2E |
| HA-11 | local path/fixture reported as generated output | record source attachments and new artifact locator |
| HA-12 | actual model silently differs from requested model | runtime model report with fallback reason |
| HA-13 | Hermes memory supplies business facts | Minora source provenance remains required |
| HA-14 | hook/API changed after Hermes upgrade | pinned compatibility suite fails closed |
