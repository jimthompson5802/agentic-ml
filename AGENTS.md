# Agent Instructions

Use Conventional Commits for commit messages: `<type>[optional scope]: <description>` (for example, `docs: update architecture proposal`).

When creating, revising, or executing detailed user-story implementation plans, follow the [planning terminology](README.md#planning-terminology) and [implementation-plan template](docs/templates/user-story-implementation-plan.md). Organize work as milestone → user story → implementation phases → granular tasks. Each implementation phase ends with an explicit developer approval gate; await approval before progressing. Approval of a written plan does not approve its implementation gates.

When scope changes during implementation-plan execution, or discovered constraints require replanning, use the [manage-plan-scope skill](.agents/skills/manage-plan-scope/SKILL.md). Record the change and decision in the affected plan's scope-change history.
