# Git Commit Instructions

Use this checklist whenever creating commits in this repository.

## Commit Checklist

- Keep commits scoped to related changes only.
- Do not include unrelated file edits.
- Ensure local changes are compatible with configured pre-commit hooks.
- Use a Conventional Commit message that matches allowed types.

## Required Commit Message Format

Format:

`<type>: <description>`

Allowed `<type>` values:

- `feat`
- `fix`
- `docs`
- `style`
- `refactor`
- `perf`
- `test`
- `build`
- `ci`
- `chore`
- `revert`

Examples:

- `docs: update swap config diagrams for 32GB setup`
- `fix: handle missing config file in parser`
- `chore: align formatting with pre-commit hooks`

## Recommended Local Flow

```bash
git --no-pager status --short --branch
git add <files>
git commit -m "<type>: <description>"
```

If hooks auto-modify files during commit, re-stage and commit again:

```bash
git add <files>
git commit -m "<type>: <description>"
```

## Notes

- `conventional-pre-commit` validates the commit message at `commit-msg` stage.
- Do not claim checks/tests were run unless they were actually run.
