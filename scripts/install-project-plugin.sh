#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
target="${1:-$PWD/.hermes/plugins/minora-hermes-adapter}"
mkdir -p "$(dirname "$target")"
rm -rf "$target"
cp -R "$repo_root/hermes_plugin" "$target"
echo "Installed project plugin at $target"
echo "Set MINORA_CONTROL_PLANE_ROOT and enable project plugins using the installed Hermes version's supported mechanism."
