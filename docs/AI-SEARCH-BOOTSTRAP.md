# AI Search profile bootstrap — 0.1.0

The generic installer lives here; the private domain workflows live in Minora-Skills, `products/ai-search-us`. This file does not embed Company Brain content or change the campaign plugin.

## Contract

Python 3.10+. Invoke the script through its interpreter. The default is a no-write preview:

```bash
python -B scripts/ai_search_bootstrap.py --bundle /absolute/approved/ai-search-us
```

After inspecting that preview, install a NEW named profile:

```bash
python -B scripts/ai_search_bootstrap.py --bundle /absolute/approved/ai-search-us --apply
```

`--hermes-root` can select a dedicated absolute Hermes root. It must match the host's actual deployment configuration. Do not use this option to pretend a directory is an OS sandbox.

The script verifies a SHA-256 manifest and exact eight-skill inventory, stages only allowlisted payload files, and invokes the installed CLI's native `profile install LOCAL_DIR --name minora-ai-search-us --yes`. It detects CLI capability and records the observed version. It does not guess compatibility with a nonexistent command or update Hermes itself. It then checks actual installed contents/configuration, root-profile integrity and absence of copied credentials/memory.

The distribution manifest explicitly owns itself plus curated skills, knowledge, scripts, contracts, fixtures, SOUL, configuration and the no-bundled-skills marker. No private git history is installed. Repeating the exact release checks integrity without replacing user credentials. A different release, unmanaged target or local managed-file drift stops rather than overwriting. An interrupted install is retained for inspection; no blind recursive deletion.

## Environment and authority

No API values are included. Configure model and optional data providers in the new profile using the secure host flow. Presence of configuration is not proof that a provider works. No model calls, paid search requests, gateway startup, new MCPs, system packages, cron jobs or external writes occur during bootstrap.

The profile allows selected web/browser/file/terminal/skill tools for read-only audit work and local artifact creation. Prompt/config restrictions are NOT a filesystem or network security boundary. Before handing access to another person, isolate the **whole Hermes process** with a dedicated OS user/VM/container and real permissions. Do not mount the founder's vault, credentials, other profiles or repository .git databases into that runtime. Do not expose a shared administrative dashboard.

Use a neutral working directory when launching Hermes. Never launch it from the Minora-Skills repository root: that root contains an unrelated campaign plugin. Only the curated product subtree is a distribution payload.

## Compatibility and upgrade policy

This is a native procedural read-only profile, not a new campaign Control Plane adapter. It does not load the legacy v0.19 plugin, register unknown campaign skills or fabricate task IDs/gates. Current official native distribution behavior is the installer contract; the exact recipient build still needs a live installation/tool-schema smoke test.

Do not pass `URL#commit` as if native distribution pinning were supported. Use a verified git checkout at the exact commit and install the local product directory. Do not call generic `profile update` against the staging directory. New releases require a reviewed migration and profile backup outside the Git repository; v0.1.0 intentionally refuses in-place forced upgrades.

## Verification

```bash
python -B -m unittest discover -s tests -p 'test_ai_search_bootstrap.py' -v
```

The 27 new tests simulate the native CLI boundary; they are not live Hermes E2E. The older repository suite and configured external providers have separate test requirements. Read the domain pack's `LIVE_ACCEPTANCE.md` before enabling access. Installer success explicitly returns `nick_access_ready: false` and names the remaining provider, isolation and gateway checks.

Primary references (reviewed 2026-09-20):
- https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions
- https://hermes-agent.nousresearch.com/docs/reference/profile-commands
- https://hermes-agent.nousresearch.com/docs/user-guide/profiles
- https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference
