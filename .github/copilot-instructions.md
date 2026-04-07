# Copilot Instructions for Playground

## Project Context

- Python project managed with Poetry.
- Target runtime is Python `>=3.12,<3.15`.
- Repository includes scripts, notebooks, and docs; prefer minimal, scoped edits.

## Coding Conventions

- Add or preserve type hints in new/modified Python code.
- Keep code clear and explicit; avoid broad refactors unless requested.
- Keep line lengths compatible with Ruff settings (`120`).
- Follow existing import/style conventions in touched files.

## Dependency and Environment Workflow

- Use Poetry for all dependency and run commands.
- Prefer commands like:
  - `poetry install`
  - `poetry run python <script>.py`
  - `poetry run jupyter notebook <notebook>.ipynb`

## Quality and Validation

- Keep changes compatible with repository hooks/tools (as configured in this repo).
- For code changes, propose a minimal validation step and exact command(s).
- Do not claim tests/checks were run unless they were actually run.

## Documentation Expectations

- Update `README.md` when adding user-facing scripts, notebooks, or docs.
- Keep markdown concise, with copyable command examples.
- Update this file (`.github/copilot-instructions.md`) with lessons learned from Copilot sessions when new guidance
  would improve future outcomes.

## Scope and Safety

- Do not change unrelated files.
- Preserve existing behavior unless a behavior change is explicitly requested.
- Ask before making destructive or environment-wide changes.

## Copilot Session Lessons Learned

Use this section to capture concise, reusable guidance discovered during sessions.

### Template

- Date: `YYYY-MM-DD`
- Context: Short description of the task/session.
- Lesson: What guidance should be reused next time.
- Action: Exact instruction added/updated in this file.
