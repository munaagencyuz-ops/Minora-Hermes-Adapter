# Installation

1. Install the sibling `Minora-Control-Plane` package.
2. Install this adapter package.
3. Copy or symlink `hermes_plugin/` into the supported Hermes project/user plugin directory.
4. Set `MINORA_CONTROL_PLANE_ROOT`, `MINORA_CONTROL_PLANE_DB`, and `MINORA_SKILLS_ROOT` outside source control.
5. Enable the plugin using the installed Hermes version's supported command.
6. Configure each profile's model and exact skill access.
7. Remove raw Minora task-creation bypasses from the coordinator profile.
8. Run plugin discovery, tool visibility, Kanban smoke, and live E2E checks.

Never commit Vertex credentials, ADC files, access tokens, runtime SQLite databases, or customer artifacts.
