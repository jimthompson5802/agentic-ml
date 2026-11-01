# Development guide reorganization

Source: approved conversation plan, 2026-11-01. Standalone documentation maintenance.

## Section preservation inventory

| Original section | Destination |
|---|---|
| Prerequisites and platform status | docs/development/setup.md |
| Clone and install the development environment | docs/development/setup.md |
| Shared development commands | docs/development.md |
| Local milestone acceptance selection | docs/development/verification.md |
| Local parallel test execution | docs/development/verification.md |
| Phase and story verification | docs/development/verification.md |
| Configuration, credentials, and troubleshooting | docs/development/setup.md |
| Repository-local Codex command approvals | docs/development/command-approvals.md |
| Python conventions and enforcement | docs/development.md |
| Suppressions and check exclusions | docs/development.md |
| Development CI and diagnostic logs | docs/development/ci.md |
| Retained development records | docs/development/records.md |
| Distribution builds and installed verification | docs/development/distribution.md |

## Validation

All moved section bodies match the original after relative-link rebasing. Local links and fragments in changed navigation and new references resolve. Original section headings remain available.

- `docs/development.md`: 3990 → 874 words; 30375 → 6996 bytes.
- `AGENTS.md`: 1700 → 1649 words; 13673 → 13302 bytes.

Reading scenarios: Python change loads core plus verification and records when testing; environment setup loads core plus setup; test gate loads core, verification and records; packaging change adds distribution; CI failure adds CI and applicable verification; evidence cleanup loads core plus records. GitHub reads additionally load command approvals. Multiple triggers accumulate.

No executable behavior changed. TDD, product tests, builds and shared executable checks are inapplicable. Existing milestone verification deferrals remain unchanged. External URLs were preserved, not live-checked.

Whitespace verification: initial extra EOF blank line corrected; final `git diff --check` passed.
