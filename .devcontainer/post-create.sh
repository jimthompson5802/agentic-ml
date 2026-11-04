#!/usr/bin/env bash
set -euo pipefail

# Configure commit attribution for the container user.
git config --global user.name 'Jim Thompson'
git config --global user.email 'jimthompson5802@gmail.com'

# Use the existing GPG signing key through VS Code's host-agent forwarding.
git config --global gpg.format openpgp
git config --global gpg.program /usr/bin/gpg
git config --global user.signingkey '514503114FA7366E'
git config --global commit.gpgsign true

# Seed the persistent Codex home while preserving container-only files.
mkdir -p /home/vscode/.codex/skills /home/vscode/.codex/rules
cp /tmp/host-codex/config.toml /home/vscode/.codex/config.toml
cp -R /tmp/host-codex/skills/. /home/vscode/.codex/skills/
cp -R /tmp/host-codex/rules/. /home/vscode/.codex/rules/

bash -lc 'source /usr/local/share/nvm/nvm.sh && nvm use default && npm install -g @openai/codex'
uv sync --locked

echo 'Start Codex with: codex --no-alt-screen (for terminal scrollback and copying text).'
