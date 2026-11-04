
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Install Node.js and npm through a Dev Container feature
# (configured in devcontainer.json).

# Install core utilities, including sleep
RUN apt-get update \
    && apt-get install -y --no-install-recommends coreutils gnupg2\
    && rm -rf /var/lib/apt/lists/*


# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.13.6 \
    /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy

ENV PATH="/usr/local/share/nvm/current/bin:/home/vscode/.npm-global/bin:${PATH}"

# Codex CLI is installed in postCreateCommand
# so it runs as the non-root vscode user.
