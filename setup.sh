#!/usr/bin/env bash
# Run once BEFORE recording, from inside this folder.
set -e
python3 -m venv .venv
.venv/bin/pip install -q -r requirements-dev.txt
git init -q 2>/dev/null || true
git config user.name "Dev"
git config user.email "dev@example.com"
echo "Prep done. Open this folder in VS Code and select the .venv interpreter."
